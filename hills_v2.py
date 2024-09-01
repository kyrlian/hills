# DRAFT

def p_change(x:int, y:int):
   p= .6
   return p

def p_up_stay_down(x, y):
   if y < summit:
      return 0.2, .2, .6
   else:
      return .6, .2, .2

def go_up_stay_down(x, y, last):
     if math.rand(1) > p_change(x,y):
         return last
     else:
         r2=rand(1)
         d, s, u =  p_up_stay_down(x, y)
         if r2 < d :
             return -1
          elif r2 < s:
             return 0
          else :
             return 1