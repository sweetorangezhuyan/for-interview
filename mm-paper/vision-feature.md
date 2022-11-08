# CSWin
![picture](images/cswin-model.png) {:height="100px" width="400px"}
## compare with self-attention
1.使用Cross-Shaped Window自注意力取代自注意力机制
2.LePE 位置编码
## Cross-Shaped Window self-attention
通过在形成十字形窗口的水平和垂直条纹中平行执行自注意力来实现。

水平方向
![picture](images/formula.png)
垂直方向
$X∈R^{(H×sw)×C}$ ，$d_k=C/K$,$K$是多头的头
## 位置编码
![picture](images/cswin_position.png)
## CSwin block
![picture](images/block.png)
![picture](images/block_f.png)
## 结构
![picture](images/architecture.png)
![picture](images/different_ar.png)
# R(2+1)D video understanding model
2维卷积后跟1维卷积,把空间和时间分解到两个阶段

$x\in R^{3\times L\times H\times W}$, $3$ is **RGB** channel, $L$ is the number of frames in clips.

$z_i$ is the output tensor of the $i-th$ convolutional block

$$z_i=z_{i-1}+F(z_{i-1};\theta_i)$$


由 $M_i$（ $N_{i-1}\times 1\times d\times d$ ）个2D卷积过滤器和 $N_i$（ $M_{i}\times t\times 1\times 1$ ）个时间卷积过滤器

$M_i=\left \lfloor \frac{td^2N_{i-1}N_i}{d^2N_{i-1}+tN_i}  \right \rfloor $, 向下取整

## 相对于3D-CNN的优势
1.在2D和1D卷积之间添加**ReLU**使网络中的非线性数量增加了一倍，增加了特征函数的复杂性，通过应用多个较小的过滤器来近似大过滤器的效果。
2.将 3D 卷积强制分为空间和时间使优化更容易。分解空间和时间使优化更加容易。
