import time
from scapy.all import sniff, IP, TCP, UDP, ICMP
from src.features import PacketFeatures


def parse_packet(pkt) -> PacketFeatures:
    """Extrae features de un paquete Scapy."""
    features = PacketFeatures(timestamp=time.time())

    if IP in pkt:
        features.src_ip = pkt[IP].src
        features.dst_ip = pkt[IP].dst
        features.src_bytes = len(pkt)

        if TCP in pkt:
            features.protocol = "tcp"
            features.src_port = pkt[TCP].sport
            features.dst_port = pkt[TCP].dport
            features.flags = str(pkt[TCP].flags)
        elif UDP in pkt:
            features.protocol = "udp"
            features.src_port = pkt[UDP].sport
            features.dst_port = pkt[UDP].dport
        elif ICMP in pkt:
            features.protocol = "icmp"

    return features


def start_capture(callback, interface: str = None, packet_count: int = 0):
    """
    Inicia la captura en tiempo real.
    callback: función que recibe cada PacketFeatures
    interface: None = todas las interfaces
    packet_count: 0 = infinito
    """
    def _process(pkt):
        if IP in pkt:
            features = parse_packet(pkt)
            callback(features)

    sniff(
        iface=interface,
        prn=_process,
        store=False,
        count=packet_count,
        filter="ip"
    )
