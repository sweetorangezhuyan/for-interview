'''
爱心程序
'''
import random
from math import cos,sin,pi,log
from tkinter import *
canvas_width=1300
canvas_height=1300
canvas_center_x=canvas_width/2
canvas_center_y=canvas_height/2
image_enlarge=30
heart_color='#e77c8e'

def heart_function(t,shrink_ratio=image_enlarge):
    # create heart
    x=16*(sin(t)**3)

    y=-(13*cos(t)-5*cos(2*t)-2*cos(3*t)-cos(4*t))
    # enlarge
    x*=shrink_ratio
    y*=shrink_ratio
    # move to the center of canvas
    x+=canvas_center_x
    y+=canvas_center_y

    return int(x),int(y)

def scatter_inside(x,y,beta=0.5):
    '''
    随机内部扩散
    x: original x
    y: original y
    beta: strong
    return: new x,y
    '''
    ratio_x=-beta*log(random.random())
    ratio_y=-beta*log(random.random())
    dx=ratio_x*(x-canvas_center_x)
    dy=ratio_x*(y-canvas_center_y)

    return x-dx,y-dy
def shrink(x,y,ratio):
    force=-1/(((x-canvas_center_x)**2+(y-canvas_center_y)**2)**0.6)
    dx=ratio*force*(x-canvas_center_x)
    dy=ratio*force*(y-canvas_center_y)

    return x-dx,y-dy
def curve(p):
    ## 自定义曲线函数，调整跳数周期
    return 2*(3*sin(4*p))/(2*pi)

class Heart:
    def __init__(self,generate_frame=20) -> None:
        self._points=set()# 原始爱心坐标集合
        self._edge_diffusion_points=set()# 边缘扩散效果点集合
        self._center_diffusion_points=set()# 中心扩散效果点集合
        self.all_points={}#每帧动态点坐标
        self.build(2000)
        self.random_halo=1000
        self.generate_frame=generate_frame
        for frame in range(generate_frame):
            self.calc(frame)
    def build(self,number):
        # heart
        for _ in range(number):
            t=random.uniform(0,2*pi)
            x,y=heart_function(t)
            self._points.add((x,y))
        # heart diffusion
        for _x,_y in list(self._points):
            for _ in range(3):
                x,y=scatter_inside(_x,_y,0.5)
                self._edge_diffusion_points.add((x,y))
        # heart diffusion once again
        point_list=list(self._points)
        for _ in range(4000):
            x,y=random.choice(point_list)
            x,y=scatter_inside(x,y,0.17)
            self._center_diffusion_points.add((x,y))
        
    @staticmethod
    def calc_position(x,y,ratio):

        force=1/(((x-canvas_center_x)**2+(y-canvas_center_y)**2)**0.520)
        dx=ratio*force*(x-canvas_center_x)+random.randint(-1,1)
        dy=ratio*force*(y-canvas_center_y)+random.randint(-1,1)

        return x-dx,y-dy
    def calc(self,generate_frame):
        ratio=10*curve(generate_frame/10*pi)
        halo_radius=int(4+6*(1+curve(generate_frame/10*pi)))## 光环
        halo_number=int(3000+4000*abs(curve(generate_frame/10*pi)**2))

        all_points=[]

        # 光环
        heart_halo_point=set()
        for _ in range(halo_number):
            t=random.uniform(0,2*pi)
            x,y=heart_function(t,shrink_ratio=11.6)
            x,y=shrink(x,y,halo_radius)
            if (x,y) not in heart_halo_point:
                heart_halo_point.add((x,y))
                x+=random.randint(-14,14)
                y+=random.randint(-14,14)

                size=random.choice((1,2,2))
                all_points.append((x,y,size))
        
        #轮廓
        for x,y in self._points:
            x,y=self.calc_position(x,y,ratio)
            size=random.randint(1,3)
            all_points.append((x,y,size))

        #内容
        for x,y, in self._center_diffusion_points:
            x,y=self.calc_position(x,y,ratio)
            size=random.randint(1,2)
            all_points.append((x,y,size))

        for x,y in self._center_diffusion_points:
            x,y=self.calc_position(x,y,ratio)
            size=random.randint(1,2)
            all_points.append((x,y,size))
        self.all_points[generate_frame]=all_points
    def render(self,render_canvas,render_frame):
        #print(self.all_points[0][1])
        for x,y,size in self.all_points[render_frame%self.generate_frame]:
            render_canvas.create_rectangle(x,y,x+size,y+size,width=0,fill=heart_color)

def draw(main,render_canvas,render_heart,render_frame=0):
    render_canvas.delete('all')
    render_heart.render(render_canvas,render_frame)
    render_canvas.create_text(650,650,text='',fill='#e77c8e',font=('微软雅黑',20,'bold'))
    main.after(160,draw,main,render_canvas,render_heart,render_frame+1)

if __name__=='__main__':
    root=Tk()
    root.title('test')
    canvas=Canvas(root,bg='white',height=canvas_height,width=canvas_width)
    canvas.pack()
    heart=Heart()
    draw(root,canvas,heart)
    root.mainloop()




