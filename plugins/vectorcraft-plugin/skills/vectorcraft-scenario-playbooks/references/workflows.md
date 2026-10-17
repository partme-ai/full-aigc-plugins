# VectorCraft 场景步骤

所有数值与文案是完整演示输入，不是用户品牌或数据。每条默认新图，组合场景需重新安排位置和选择范围。

## approval-check-badge：可编辑审核通过徽章

输入：240×240屏幕画板，绿色圆底和白色勾号；不是认证标识。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"可编辑审核通过徽章","width":240,"height":240,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建底圆 | `shape.ellipse` | `{"x":20,"y":20,"width":200,"height":200}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#16804a"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 创建未闭合勾号路径 | `path.create` | `{"d":"M 65 120 L 105 160 L 180 80"}` |
| 6. 开放路径不填充 | `paint.setFill` | `{"none":true}` |
| 7. 设置白色线条 | `paint.setStroke` | `{"color":"#ffffff"}` |
| 8. 设置圆端点与圆连接 | `stroke.set` | `{"weight":16,"cap":"round","join":"round"}` |

检查：圆与勾号保留独立编辑；勾号路径未闭合且白色描边宽16；缩小后检查识别度。

边界：示例仅图形制作，不意味着获得第三方批准或认证。

## editable-three-bar-chart：可编辑三项数据柱图

输入：A=30、B=55、C=80，线性比例1.5像素/单位，共同零基线y=200。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"可编辑三项数据柱图","width":400,"height":250,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建可编辑矩形 | `shape.rectangle` | `{"x":60,"y":155.0,"width":48,"height":45.0}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 创建可编辑文字 | `text.create` | `{"x":72,"y":225,"text":"A","size":16,"font":"Arial","color":"#172033"}` |
| 6. 创建可编辑文字 | `text.create` | `{"x":60,"y":145.0,"text":"30","size":14,"font":"Arial","color":"#172033"}` |
| 7. 创建可编辑矩形 | `shape.rectangle` | `{"x":160,"y":117.5,"width":48,"height":82.5}` |
| 8. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#16a34a"}` |
| 9. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 10. 创建可编辑文字 | `text.create` | `{"x":172,"y":225,"text":"B","size":16,"font":"Arial","color":"#172033"}` |
| 11. 创建可编辑文字 | `text.create` | `{"x":160,"y":107.5,"text":"55","size":14,"font":"Arial","color":"#172033"}` |
| 12. 创建可编辑矩形 | `shape.rectangle` | `{"x":260,"y":80.0,"width":48,"height":120.0}` |
| 13. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#d97706"}` |
| 14. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 15. 创建可编辑文字 | `text.create` | `{"x":272,"y":225,"text":"C","size":16,"font":"Arial","color":"#172033"}` |
| 16. 创建可编辑文字 | `text.create` | `{"x":260,"y":70.0,"text":"80","size":14,"font":"Arial","color":"#172033"}` |

检查：柱高按数值比例且同零基线；类别和值仍是文字；数据来源和单位按真实任务补齐。

边界：这是可编辑图元而非具有数据绑定的原生图表；数据更新时同步重算柱高和文字，不能截断基线误导比较。

## hollow-ring-minus-front：真实镂空圆环

输入：外圆160内圆80，先外后内；共同中心120,120。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"真实镂空圆环","width":240,"height":240,"units":"Pixels","backgroundContents":"white"}` |
| 2. 先创建后方外圆 | `shape.ellipse` | `{"x":40,"y":40,"width":160,"height":160}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 再创建前方切除圆 | `shape.ellipse` | `{"x":80,"y":80,"width":80,"height":80}` |
| 6. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 7. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 8. 只在本例独立新图选择本次全部对象 | `select.all` | `{}` |
| 9. 前圆从后圆相减，生成真实镂空 | `object.pathfinder.minusFront` | `{}` |
| 10. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 11. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |

检查：中心透明/底色透出且环带存在；不是白圆盖住蓝圆；SVG保留复合路径。

边界：已有图纸用实际两圆ID调用select.set，不可select.all；反向堆叠会产生不同结果。

## contact-card-layout：屏幕联系卡排版

输入：360×200画板，示例姓名、职责和占位邮箱，真实任务替换全部文案。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"屏幕联系卡排版","width":360,"height":200,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建可编辑矩形 | `shape.rectangle` | `{"x":0,"y":0,"width":360,"height":200}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#f1f5f9"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 创建可编辑矩形 | `shape.rectangle` | `{"x":0,"y":0,"width":12,"height":200}` |
| 6. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 7. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 8. 创建可编辑文字 | `text.create` | `{"x":36,"y":65,"text":"Ada Chen","size":28,"font":"Arial","color":"#172033"}` |
| 9. 创建可编辑文字 | `text.create` | `{"x":36,"y":105,"text":"Designer","size":18,"font":"Arial","color":"#172033"}` |
| 10. 创建可编辑文字 | `text.create` | `{"x":36,"y":150,"text":"ada@example.test","size":16,"font":"Arial","color":"#172033"}` |

检查：姓名、职责和联系方式均可编辑；文字未越出画板；占位数据已替换后再交付。

边界：此例是屏幕卡片，不是已配置出血、CMYK和印厂要求的印刷名片。

## editable-brand-palette：品牌色板与十六进制标签

输入：4个示例sRGB色，标签必须与填色一致。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"品牌色板与十六进制标签","width":440,"height":180,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建可编辑矩形 | `shape.rectangle` | `{"x":20,"y":30,"width":80,"height":80}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#172033"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 创建可编辑文字 | `text.create` | `{"x":20,"y":140,"text":"#172033","size":13,"font":"Arial","color":"#172033"}` |
| 6. 创建可编辑矩形 | `shape.rectangle` | `{"x":120,"y":30,"width":80,"height":80}` |
| 7. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#2563eb"}` |
| 8. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 9. 创建可编辑文字 | `text.create` | `{"x":120,"y":140,"text":"#2563eb","size":13,"font":"Arial","color":"#172033"}` |
| 10. 创建可编辑矩形 | `shape.rectangle` | `{"x":220,"y":30,"width":80,"height":80}` |
| 11. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#16a34a"}` |
| 12. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 13. 创建可编辑文字 | `text.create` | `{"x":220,"y":140,"text":"#16a34a","size":13,"font":"Arial","color":"#172033"}` |
| 14. 创建可编辑矩形 | `shape.rectangle` | `{"x":320,"y":30,"width":80,"height":80}` |
| 15. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#d97706"}` |
| 16. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 17. 创建可编辑文字 | `text.create` | `{"x":320,"y":140,"text":"#d97706","size":13,"font":"Arial","color":"#172033"}` |
| 18. 只在本例独立新图选择本次全部对象 | `select.all` | `{}` |
| 19. 将本次色板与标签归组 | `object.group` | `{}` |

检查：四个色块与四个标签对应；组内对象仍可编辑；不把普通RGB色块说成全局专色色板。

边界：这不是印刷色样或自动全局色同步；已有图纸按返回ID归组，不选中其他用户内容。

## wordmark-live-and-outlined：文字标志母版与轮廓交付

输入：示例文字CRAFT，Arial字体；先确认实际字体存在和使用授权。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"文字标志母版与轮廓交付","width":420,"height":160,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建可编辑文字 | `text.create` | `{"x":30,"y":105,"text":"CRAFT","size":64,"font":"Arial","color":"#172033"}` |
| 3. 转轮廓前保存可编辑文字母版 | `file.save` | `{"path":"wordmark-live.vectorcraft"}` |
| 4. 保持当前文字选区并转成字形路径 | `type.createOutlines` | `{}` |
| 5. 显式另存轮廓交付，避免普通保存覆盖活文字母版 | `file.save` | `{"path":"wordmark-outlined.vectorcraft"}` |

检查：母版仍含CRAFT文字；独立新图交付工程无活文字且含轮廓；既有图仅检查本次文字，其他文字保留可编辑；母版与轮廓版文件名不同。

边界：转轮廓不可当成仍可改字；不能仅保存最终轮廓而丢失母版。固定母版路径是新目录示例，真实任务用未占用路径。

## half-disc-real-crop：半圆图标的真实几何裁切

输入：160×160圆位于40,40，裁切保留左半范围[40,40,80,160]。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"半圆图标的真实几何裁切","width":240,"height":240,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建完整圆形 | `shape.ellipse` | `{"x":40,"y":40,"width":160,"height":160}` |
| 3. 设置当前新建对象填色 | `paint.setFill` | `{"color":"#7c3aed"}` |
| 4. 去除当前对象描边 | `paint.setStroke` | `{"none":true}` |
| 5. 只裁切当前新建对象 | `path.rectCut` | `{"rect":[40,40,80,160]}` |

检查：保留几何边界宽80高160；右侧像素为底色；不存在仅遮住右半的裁切蒙版。

边界：真实几何裁切会丢弃裁切外路径；在副本操作，原圆若需复用先保留源工程。

## wayfinding-arrow：带方向箭头的导视线

输入：从40,100到220,100的水平向右导视线，箭头端点对齐终点。

| 顺序与目的 | 方法 | 参数 |
| --- | --- | --- |
| 1. 仅新建独立场景时建立画板 | `file.new` | `{"name":"带方向箭头的导视线","width":280,"height":160,"units":"Pixels","backgroundContents":"white"}` |
| 2. 创建开放导视路径 | `path.create` | `{"d":"M 40 100 L 220 100"}` |
| 3. 开放路径无填充 | `paint.setFill` | `{"none":true}` |
| 4. 设置深色导视描边 | `paint.setStroke` | `{"color":"#172033"}` |
| 5. 设置箭头与端点对齐 | `stroke.set` | `{"weight":8,"cap":"round","endArrow":"Triangle","arrowAlign":"tip"}` |
| 6. 创建可编辑文字 | `text.create` | `{"x":40,"y":55,"text":"GO","size":24,"font":"Arial","color":"#172033"}` |

检查：箭头朝右且保留描边参数；GO文字可编辑；箭头端点对齐不超出目的端。

边界：箭头实际指向须按场地路线确认，本例不代表已完成无障碍或安全导视设计。

