from .__c import include, C, c, structure 

__all__ = ['C', 'c', 'include', 'structure']

__doc__ = """

    @structure(1024)
    class py_ip_pack(C):
        _raw = \"\"\"
    typedef struct ip_packet{
        long ip_len;
        long payload_len;
        char src[16] ;
        char dst[16] ;
        u_char protocol;
        u_char payload[1500];
    } py_ip_pack; 
    \"\"\"
        pass

example inlcude:

# will auto load libsniff.so's all functions which if it is in libsniff.h
@include(qlib_c_lib_header_path, LibStructure)
class libsniff:
	
    @c #this decorator will auto trans py's type to ctypes
    def __init__(self, dev):
        libsniff.init_pcap(dev)





"""
