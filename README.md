# E3Config
Easy and Effective Experiment config tool

本工具主要用于简化运行算法离线实验时，需要不停调整超参数，以及由超参数修改带来的其他修改。

本工具使用json作为配置文件载体，通过设置规则和对应的解析方法，实现以下功能
1.原始配置有多层嵌套，但是解析后的结果是简单的dict对象，没有嵌套。
2.每个配置项需要设置一个默认值，并支持在不同的条件下有不同的值。
3.具备简单的字符串、算术计算功能。