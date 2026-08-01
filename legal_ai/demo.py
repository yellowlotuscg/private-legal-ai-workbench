from .retrieval import Passage,retrieve
def main():
 ps=[Passage("matter-a","contract.md","The agreement renews annually unless notice is given thirty days before renewal."),Passage("matter-b","memo.md","The payment dispute was referred to mediation.")]
 hits=retrieve("renewal notice",ps,"matter-a")
 print({"answer_supported":bool(hits),"citations":[h.source for h in hits],"matter_boundary":"matter-a"})
if __name__=="__main__": main()
