from machine import Pin, SoftSPI
import GFX
import SSD1331


class ScreenWrite:
    
    def __init__(self, txtc=96315, lblc=0x000000, bgc=0xffffff):
        self.txtc = txtc
        self.lblc = lblc
        self.bgc = bgc
        
        
    def textColorUpdate(self, txtc=96320):
        self.txtc = txtc
    
    
    def labelColorUpdate(self, lblc=0x000000):
        self.lblc = lblc
    
    
    def backgroundColorUpdate(self, bgc=0xffffff):
        self.bgc = bgc
    
    
    def backgroundRefresh(self, display):
        display.fill(self.bgc)
    
    
    def labels(self, gfx): # Add color options later
        label_x_indices_BPM = [0,0,0,0,0,1,1,1,2,2,4,4,4,4,4,5,5,6,8,8,8,8,8,9,10,10,10,10,10,11,12,12,12,12,12]
        label_y_indices_BPM = [0,1,2,3,4,0,2,4,1,3,0,1,2,3,4,0,2,1,0,1,2,3,4,0,0,1,2,3,4,0,0,1,2,3,4]
        
        label_x_indices_colons = [43,43,91,91]
        label_y_indices_colons = [1,3,1,3]
        
        label_x_indices_O2 = [0,0,0,1,1,2,2,3,3,3,5,5,5,6,6,6,7,7,9,9,10,11,11]
        label_y_indices_O2 = [1,2,3,0,4,0,4,1,2,3,0,3,4,0,2,4,1,4,0,3,2,1,4]
        
        for i in range(len(label_x_indices_BPM)): # BPM
            gfx.fill_rect(2+label_x_indices_BPM[i]*3,2+label_y_indices_BPM[i]*3,3,3,self.lblc)
            
        for i in range(len(label_x_indices_colons)): # colons
            gfx.fill_rect(label_x_indices_colons[i],2+label_y_indices_colons[i]*3,3,3,self.lblc)
        
        for i in range(len(label_x_indices_O2)): # O2
            gfx.fill_rect(52+label_x_indices_O2[i]*3,2+label_y_indices_O2[i]*3,3,3,self.lblc)
            
        gfx.rect(48,0,2,64,self.lblc)
    
    
    def numberRefresh(self,gfx):
        # BPM Numbers
        gfx.fill_rect(5,31,10,18,0) # 1st
        gfx.fill_rect(18,31,10,18,0) # 2nd
        gfx.fill_rect(31,31,10,18,0) # 3rd
        
        #O2 Numbers
        gfx.fill_rect(55,31,10,18,0) # 1st
        gfx.fill_rect(68,31,10,18,0) # 2nd
        gfx.fill_rect(81,31,10,18,0) # 3rd
    
    
    def write(self,gfx,bpm="000",o2="000"):
        self.numberRefresh(gfx)
        BPM_x0 = [5,18,31]  
        O2_x0 = [55,68,81]

        for i in range(3):
            self.draw(gfx,BPM_x0[i],31,int(bpm[i]))
            self.draw(gfx,O2_x0[i],31,int(o2[i]))
        
    def draw(self,gfx,x0,y0,num):
        if num == 0:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0,y0+10,2,6,self.txtc) # bottom left
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 1:
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            
        elif num == 2:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0,y0+10,2,6,self.txtc) # bottom left
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 3:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 4:
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            
        elif num == 5:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 6:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0,y0+10,2,6,self.txtc) # bottom left
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 7:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            
        elif num == 8:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0,y0+10,2,6,self.txtc) # bottom left
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        elif num == 9:
            gfx.rect(x0+2,y0,6,2,self.txtc) # top middle
            gfx.rect(x0,y0+2,2,6,self.txtc) # top left
            gfx.rect(x0+8,y0+2,2,6,self.txtc) # top right
            gfx.rect(x0+2,y0+8,6,2,self.txtc) # middle
            gfx.rect(x0+8,y0+10,2,6,self.txtc) # bottom right
            gfx.rect(x0+2,y0+16,6,2,self.txtc) # bottom middle
            
        else:
            raise Exception("Method draw() of ScreenWrite received a value that isn't a value between 0 and 9")