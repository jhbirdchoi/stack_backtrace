# stack_backtrace

这个小工具是为解决采用小系统的嵌入式系统调试困难做的。

- 时间大概在2010年左右，当时的系统是ARM9，上面跑的是或者是裸系统，或者是 *cosII之类的小系统；
- 这些系统，对于死机之后，调试信息非常不友好，在跑稳定性的时候，很难定位到挂掉的地方；
- 于是就有了这个小工具。

## 思路

* ARM体系，如果出现异常指令，将触发相应的中断
	- 通常和软件异常相应的中断有：未定义指令异常/预取指令中止/数据中止 等等
* 进入中断之后，打印出各个「线程的栈」信息，供后续分析；
* 在rvds 2.2 下stack的布局：

>
	high addr
        --------------------------
        frame1
              <R0, .. R10>  (可选)
              R14  (返回地址)
        frame2
               <R0, .. R10>  (可选)
              R14   (返回地址)
            ...............
        --------------------------
    low addr


* 由于这样的stack信息不足，不像X86体系，无SP信息。
  这里用近似的做法，dump的数据，数值只要 .text段地址范围内，就认为是返回地址。

## 使用例子

>
python stackBacktrace.py exam/map.txt exam/stack.tx

可能的结果

>
	stack 1
	0x60126dd4, [two_func, 0x60126dc4, 0x28]
	0x60126df0, [one_func, 0x60126de0, 0x32]
	0x60126e10, [zero_func, 0x60126e00, 0x192]
	0x601273dc, [NetVideoWinCommProc, 0x60126f8c, 0x1248]
	0x600a8c0c, [IWindowDispatchMessageProcList, 0x600a8bb8, 0x160]
	0x600a8248, [IWindowCallMsgHandle, 0x600a8218, 0x68]
	0x600a8c0c, [IWindowDispatchMessageProcList, 0x600a8bb8, 0x160]
	0x600a8c8c, [IWindowDispatchMessage, 0x600a8c58, 0x88]
	0x60144c24, [ButtonPngTouchPro, 0x60144bd4, 0x108]
	0x600a8248, [IWindowCallMsgHandle, 0x600a8218, 0x68]
	0x600a8c0c, [IWindowDispatchMessageProcList, 0x600a8bb8, 0x160]
	0x600a8c8c, [IWindowDispatchMessage, 0x600a8c58, 0x88]
	0x600a9a4c, [IWindowTouchMessageDispatch, 0x600a99e0, 0x364]
	0x600aa01c, [IGuiWindowMsgHandle, 0x600a9f98, 0x660]
	0x600a9f98, [IGuiWindowMsgHandle, 0x600a9f98, 0x660]
	0x600d1b40, [TaskMsgDispatch, 0x600d1b0c, 0x100]
	0x600d1b94, [PriNormalTask, 0x600d1b70, 0x92]
	stack 2
	0x600d1b70, [PriNormalTask, 0x600d1b70, 0x92]


这样就知道了函数挂掉之的整个 **stack backtrace**，便于分析。




