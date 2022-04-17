from math import ceil, floor

class Pagination():
    def __init__(self, countItem, actPage=0, perPage=20, countResPage=15):
        self.countItem = countItem
        self.actPage = actPage
        self.perPage = perPage
        self.countResPage = countResPage
        self.maxPage=None
        self.pagSeq=None

        self._getMaxPage()
        self._getPaginationSeq()

    def _getMaxPage(self):
        self.maxPage=ceil(self.countItem/self.perPage)
        if(self.maxPage<1): self.maxPage=1
        if self.actPage==0: self.actPage=self.maxPage
    
    def _getPaginationSeq(self):
        start=self.actPage-floor(self.countResPage/2)
        if(start<1): start=1
        end=self.actPage+floor(self.countResPage/2)
        if(end>self.maxPage): end=self.maxPage
        self.pagSeq = (start,end)

    def isOutSide(self, get_param):
        return (get_param>self.maxPage or get_param<1)

