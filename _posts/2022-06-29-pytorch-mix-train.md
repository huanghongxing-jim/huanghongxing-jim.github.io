---
layout: post
category: [网络训练]
tag: [Pytorch网络训练, 自动混合精度, 经验]
title: Pytorch自动混合精度训练
---


# `autocast` + `GradScaler`

# 一、单卡例程

{% raw %}
```python
from torch.cuda import amp
model = Net() # 创建model，默认是torch.FloatTensor
optimizer = optim.SGD(model.parameters(), ...)
scaler = amp.GradScaler(enabled=True)
for epoch in epochs:
    for inputs, target in data:
        optimizer.zero_grad()
        # 前向过程(model + loss)开启 autocast
        with amp.autocast(enabled=True):
            output = model(inputs)
            loss = loss_fn(output, target)
        # 1、Scales loss.  先将梯度放大 防止梯度消失
        scaler.scale(loss).backward()
        # 2、scaler.step()   再把梯度的值unscale回来.
        # 如果梯度的值不是 infs 或者 NaNs, 那么调用optimizer.step()来更新权重,
        # 否则，忽略step调用，从而保证权重不更新（不被破坏）
        scaler.step(optimizer)
        # 3、准备着，看是否要增大scaler
        scaler.update()
        # 正常更新权重
        optimizer.zero_grad()
```
{% endraw %}

# 二、多卡并行例程

**`amp`只能在单GPU环境下使用，多卡训练需要在网络的`forward()`函数里使用`with autocast()`。**

{% raw %}
```python
class Net(nn.Module):
    def forward(self, x):
    	with autocast():
    		...
    	return
```
{% endraw %}



