---
title: the-last-dance-somethings-end-in-spring
pubDatetime: 2022-01-01T00:00:00Z
description: the-last-dance-somethings-end-in-spring
draft: false
---
title: 极速浏览器最近工作小结——Last Dance
pubDatetime: 2022-01-01T00:00:00Z
description: the-last-dance-somethings-end-in-spring

date: 2023-04-07 23:30:00

index_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/a_single_man_in_ragged_clothes_on_an_abandoned_deserted_lush_island_looking_at_the_sea_surrounded_by_a_vast_ocean.png

banner_img: https://raw.githubusercontent.com/wuruofan/image_repo/main/img/a_single_man_in_ragged_clothes_on_an_abandoned_deserted_lush_island_looking_at_the_sea_surrounded_by_a_vast_ocean.png

categories:

- 总结回顾

tags:

- 极速浏览器

---

## Last Dance



嘿，大家好。


不知道应该怎么和大家说，估计大家看到文章的时候，极速浏览器三月底的版本应该已经上线了，由于一些个人的原因，最近我离职了，离开了极速浏览器团队，所以这次更新应该就是我参与的最后一个迭代了。



改了两个陈年的播放器bug，权当作给大家的临别礼物吧。这俩bug都得有快两年了吧，之前开发留下来的，应该能解决一批播放器闪退的问题。


一个是播放器连续播放本地视频时必现的OOM问题，通常多播放一些本地视频就可能复现，和视频大小有关系。

另一个播放器外部和内核内部多个播放器id用错的问题。这个隐藏的非常深，是之前开发重构代码不完全导致的。内核代码中，网页里的一个视频播放时对应了2个不同的id，但是上层使用的时候在某些场景时会存在用错id的情况，会导致应用崩溃，崩溃的堆栈又很奇怪，着实很难定位，花了很长时间才解决。




另外，还优化了下绿e浏览器无内核mini包的逻辑，应该以后在极速版也会上线吧。

还有一个比较重要的工作，就是写了份23页上万字的内核开发总结，希望能帮到后面的内核开发同学，也算交代了下问题该怎么定位，以后该怎么处理。



能力有限，我已经尽力了。



我知道有很多朋友是因为极速浏览器关注我的，我也一直在努力，希望能做的更好一些，但还是到了要说再见的时候了。

希望极速浏览器可以越来越好。祝大家天天开心。以后应该不会更新极速浏览器相关的文章了，大家可以取消关注了。





## 未来




换了环境，目前还有一堆事情需要处理，希望自己能尽快适应新的工作吧。

以后，我可能会在业余时间写一些自用的工具类app，也有可能写一个自己的浏览器。



最近也在思考自己能利用chatgpt做些什么，大家有什么好点子也可以分享给我。

GPT帮我写了一段文字，我放在最后面了，的确很强大。另外，配图也是AI画的。😺😺





## 最后的最后



祝大家都好，希望大家继续支持极速浏览器。



![a japanese girl in modern city](https://raw.githubusercontent.com/wuruofan/image_repo/main/img/a_japanese_girl_in_modern_city_by_agnes_cecile_and_P._A._Works__Lens_reflection__detailed_vivid__Hyper_minimal.png)





## 附GPT版本：



> 尊敬的极速浏览器用户们：
>
> 我是之前负责开发极速浏览器的工程师之一，在此非常荣幸地向大家告别。我离职前的最后一个月，我专注于优化播放器的一些历史问题，解决了两年前的一个本地播放器OOM问题和一个两年前播放器内部混用ID的问题。这是我离开前的最后一项工作，也是我极速浏览器工作的一个重要里程碑。
>
> 在我的职业生涯中，我一直专注于编程领域的探索和研究。加入极速浏览器的团队后，我有幸参与了这个项目的各个方面，也积累了丰富的工作经验。我始终认为，开发者应该不断地学习和改进，以提供更好的用户体验。
>
> 在极速浏览器团队的时间里，我遇到了很多有趣的挑战，同时也结识了很多优秀的同事。在这里，我要特别感谢我的同事们，他们的支持和鼓励，帮助我度过了很多困难的时刻。此外，我还要感谢所有的用户，因为是你们对极速浏览器的支持和信任，让我们的团队不断成长和壮大。
>
> 离开极速浏览器团队并不是我的最终目的，我会继续深入探索编程领域，并且会尝试写一些小工具，或者开发一个安卓浏览器应用程序。当然，这需要一定的时间和精力，但我相信这将是一个有意义的过程。
>
> 最后，我再次感谢所有的用户和团队成员的支持和帮助，祝愿极速浏览器在未来能够越来越好，为广大用户提供更加优秀的浏览体验。如果您对我的未来有任何问题或建议，欢迎随时联系我。
>
> 再见，极速浏览器！
>
> 此致 敬礼
>
> XXX
>



<p>



以上，欢迎关注公众号“**小黑杂说**”。




![小黑杂说](https://raw.githubusercontent.com/wuruofan/wuruofan.github.io/master/img/qr-wechat-large.png)