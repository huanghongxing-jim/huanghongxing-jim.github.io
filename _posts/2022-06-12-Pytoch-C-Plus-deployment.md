---
layout: post
category: [模型部署]
tag: [Pytorch C/C++, torch.jit, 学习笔记] 
title: Pytorch C/C++模型部署
---


# 一、环境

1. 系统： `Windows 10`
2. 软件：`Visual Stuido 2019`+`VSIXTorch.vsix`。**[VSIXTorch.vsix](/assets\attachments\network-deployment-pytorch-c\VSIXTorch.vsix)** 只支持到 `Visual Studio 2019`。
3. 下载 `libtorch`：![](/assets\images\network-deployment-pytorch-c/2022-06-12-20-52-53.png)

## 二、例程

[Pytorch C++ API文档资源](https://pytorch.org/cppdocs/)

1. 建立项目，注意`inclue`目录和`lib`目录，以及lib包检测是否附到项目属性上了：
![](/assets\images\network-deployment-pytorch-c/2022-06-12-20-55-33.png)

2. 运行：  

{% raw %}
```python
import torch
import torchvision
model = torchvision.models.resnet18(pretrained=True)
example = torch.rand(1, 3, 224)
traced_script_module = torch.jit.trace(model, example)
traced_script_module.save("traced_resnet_model.pt")
```
{% endraw %}

{% raw %}
```c++
#include <torch/script.h> ​
#include <torch/torch.h> ​
#include <iostream>
#include <memory>
int main(int argc, const char* argv[]) {
    torch::jit::script::Module model;
    model = torch::jit::load("traced_resnet_model.pt", at::kCUDA);
    std::vector<torch::jit::IValue> inputs;
    inputs.push_back(torch::ones({ 1, 3, 224, 224 }, at::kCUDA));
    at::Tensor output = model.forward(inputs).toTensor();
    std::cout << output.slice(1, 0, 5) << "\n";
    return 0;
}
```
{% endraw %}

**注意：TensorFlow+Windows+Visual Studio比较麻烦，要手动搞CMake，Torch C/C++只需要用Visual Studio 2019的libtorch插件就行。**

## 三、Torch模型部署

> JIT是一种概念，全称是 Just In Time Compilation，中文译为**即时编译**，是一种程序优化的方法。TorchScript（PyTorch的JIT实现）TorchScript是Pytorch模型（继承自nn.Module）的中间表示，可以在像C++这种高性能的环境中运行。**用JIT将Python模型转换为 TorchScript Module。**
> 
> 使用Python训练模型，然后通过JIT将模型转为语言无关的模块，从而让C++可以非常方便得调用，从而把PyTorch模型部署到任意平台和设备上：树莓派、iOS、Android等。

[Torchscript文档资源](https://pytorch.org/docs/master/jit.html)  

**torch.jit有两种生成方式：torch.jit.trace和torch.jit.script，前者不能有if、while等控制流，后者可以有。**




