import os
import streamlit as st

def pcap2CSV():
    try:
        os.system('tshark -r data/test.pcap -T fields -E header=y -E separator=, -E quote=d -E occurrence=f \
                -e ip.version -e ip.hdr_len -e ip.tos -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df \
                -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e ip.checksum -e ip.src -e ip.dst \
                -e ip.len -e ip.dsfield -e tcp.srcport -e tcp.dstport -e tcp.seq -e tcp.ack -e tcp.len \
                -e tcp.hdr_len -e tcp.flags -e tcp.flags.fin -e tcp.flags.syn -e tcp.flags.reset \
                -e tcp.flags.push -e tcp.flags.ack -e tcp.flags.urg -e tcp.flags.cwr -e tcp.window_size \
                -e tcp.checksum -e tcp.urgent_pointer -e tcp.options.mss_val > data/testPacketToCSV.csv')

    except Exception as e:
        st.write(e)