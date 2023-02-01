import os
import openai

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"

#response = openai.Completion.create(
#  model="text-davinci-003",
#  #prompt="A table summarizing the fruits from Goocrux:\n\nThere are many fruits that were found on the recently discovered planet Goocrux. There are neoskizzles that grow there, which are purple and taste like candy. There are also loheckles, which are a grayish blue fruit and are very tart, a little bit like a lemon. Pounits are a bright green color and are more savory than sweet. There are also plenty of loopnovas which are a neon pink flavor and taste like cotton candy. Finally, there are fruits called glowls, which have a very sour and bitter taste which is acidic and caustic, and a pale orange tinge to them.\n\n| Fruit | Color | Flavor |",
#  #prompt="please help to translate this product title to english:梓洲蓝白五片游泳板加厚可拆卸自学游泳腰带浮力板现货大背漂蓝黄",
#  #prompt="please help to generate the key features of this product in english:真无线蓝牙耳机tws入耳式降噪耳机蓝牙无线M10低延迟游戏",
#  #prompt="write description of this prodcut with bullet points in english:真无线蓝牙耳机tws入耳式降噪耳机蓝牙无线M10低延迟游戏",
#  #prompt="please help to translate these detail information for a e-commerce product: 材质：EVA 规格：173*60*0.4 克重180G-200g左右【支持定制】：可定制，4mm，6mm，8mm的瑜伽垫，详情请咨询我司客服，欢迎来样、来图加工定做，质量好，价格低 可印刷可供LOGO ",
#  #prompt="please help to translate these detail information for a e-commerce product: 品牌魔力茉莉材质EVA 重量200（g）厚度4（mm）货号ZZ00002 产地 宁波 加工定制 是 产品类别 瑜伽垫 适用场景 健身器材,徒步登山野营,舞蹈运动 颜色 黄,紫,蓝,黑,粉色,荧光绿,深绿,橘色 规格 173*60*0.4（cm） 是否跨境出口专供货源 否 图案 纯色 尺寸 173*60*0.4CM 专利类型 无", 
#  #prompt="please generate a product title in english by these information: 跨境属性 跨境包裹重量 0.2kg 单位重量 0.152kg 商品属性 品牌 魔耳欣 货号 M10 传输范围 15米 功能 降噪,电量显示,通话功能,语音控制,支持音乐,多点连接 加工定制 是 加印LOGO 可以 蓝牙协议 5.2 声道 立体声 使用方式 耳塞式 是否单双耳 双边立体声 适用送礼场合 婚庆,生日,节日,乔迁,展销会,广告促销,员工福利,周年庆典,商务馈赠,开业典礼,颁奖纪念,公关策划 颜色 哑面黑色烫金,哑面白色烫银,哑面墨绿色烫金 主要下游平台 ebay,亚马逊,wish,速卖通,独立站,LAZADA,其他 主要销售地区 非洲,欧洲,南美,东南亚,北美,东北亚,中东 有可授权的自有品牌 是 是否跨境出口专供货源",
#  #prompt="what is the brand name of this product: 跨境属性 跨境包裹重量 0.2kg 单位重量 0.152kg 商品属性 品牌 魔耳欣 货号 M10 传输范围 15米 功能 降噪,电量显示,通话功能,语音控制,支持音乐,多点连接 加工定制 是 加印LOGO 可以 蓝牙协议 5.2 声道 立体声 使用方式 耳塞式 是否单双耳 双边立体声 适用送礼场合 婚庆,生日,节日,乔迁,展销会,广告促销,员工福利,周年庆典,商务馈赠,开业典礼,颁奖纪念,公关策划 颜色 哑面黑色烫金,哑面白色烫银,哑面墨绿色烫金 主要下游平台 ebay,亚马逊,wish,速卖通,独立站,LAZADA,其他 主要销售地区 非洲,欧洲,南美,东南亚,北美,东北亚,中东 有可授权的自有品牌 是 是否跨境出口专供货源, and please just tell me the english brand name only",
#  #prompt="write description of this prodcut with bullet points: 跨境属性 跨境包裹重量 0.2kg 单位重量 0.152kg 商品属性 品牌 魔耳欣 货号 M10 传输范围 15米 功能 降噪,电量显示,通话功能,语音控制,支持音乐,多点连接 加工定制 是 加印LOGO 可以 蓝牙协议 5.2 声道 立体声 使用方式 耳塞式 是否单双耳 双边立体声 适用送礼场合 婚庆,生日,节日,乔迁,展销会,广告促销,员工福利,周年庆典,商务馈赠,开业典礼,颁奖纪念,公关策划 颜色 哑面黑色烫金,哑面白色烫银,哑面墨绿色烫金 主要下游平台 ebay,亚马逊,wish,速卖通,独立站,LAZADA,其他 主要销售地区 非洲,欧洲,南美,东南亚,北美,东北亚,中东 有可授权的自有品牌 是 是否跨境出口专供货源", temperature=1,
#  #prompt="please remove all the html tags for this text: <div id=""titleHeader"">Anchor Ear Buckle Fashion Titanium Punk Stud Earrings</div><br>",
#  prompt="please remove all the html tags for this text, and divided the content in lines: <p style=""bullet"">DIY patch, clothing cloth patch</p><img style=""default"" width=""585"" height=""525"" src=""https://multimedia-image.s3.us-west-2.amazonaws.com/product-center-graphics/2022/05/11/93154e77-a96a-4560-b817-ec3eb600887b.jpg""><img style=""default"" width=""676"" height=""679"" src=""https://multimedia-image.s3.us-west-2.amazonaws.com/product-center-graphics/2022/05/11/5f2a05ac-4867-452d-b832-7d311e33ada9.jpg""><img style=""default"" width=""581"" height=""538"" src=""https://multimedia-image.s3.us-west-2.amazonaws.com/product-center-graphics/2022/05/11/1b06647e-fc49-49fe-920b-2e62d20c1947.jpg""><img style=""default"" width=""569"" height=""510"" src=""https://multimedia-image.s3.us-west-2.amazonaws.com/product-center-graphics/2022/05/27/d4af229d-b910-4eb6-86ca-baa180507930.jpg""><img style=""default"" width=""563"" height=""452"" src=""https://multimedia-image.s3.us-west-2.amazonaws.com/product-center-graphics/2022/05/27/41a790f3-b8a2-4a5c-911d-12c351265c2d.jpg""><div id=""titleHeader"">Diy Patch Adhesive Glue Patch Clothes Repair Cloth Stickers Denim Cloth Iron Sticker</div><br>",
#  max_tokens=300,
#  top_p=1.0,
#  frequency_penalty=0.0,
#  presence_penalty=0.0
#)
#print (response.choices[0]['text'].strip())
#
#
#body_content = response.choices[0]['text']
#prompt = "this is some information of a product, please help to genenrate a product title: %s"%body_content
#print ("...%s..."%prompt)
#response = openai.Completion.create(
#  model="text-davinci-003",
#  prompt=prompt,
#  max_tokens=300,
#  top_p=1.0,
#  frequency_penalty=0.0,
#  presence_penalty=0.0
#)
#ret = response.choices[0]['text']
#print ("the title generate by GPT-3 is: %s"%response.choices[0]['text'].strip())


print ("-----------------------")

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="what is the brand name of this product: 跨境属性 跨境包裹重量 0.2kg 单位重量 0.152kg 商品属性 品牌 魔耳欣 货号 M10 传输范围 15米 功能 降噪,电量显示,通话功能,语音控制,支持音乐,多点连接 加工定制 是 加印LOGO 可以 蓝牙协议 5.2 声道 立体声 使用方式 耳塞式 是否单双耳 双边立体声 适用送礼场合 婚庆,生日,节日,乔迁,展销会,广告促销,员工福利,周年庆典,商务馈赠,开业典礼,颁奖纪念,公关策划 颜色 哑面黑色烫金,哑面白色烫银,哑面墨绿色烫金 主要下游平台 ebay,亚马逊,wish,速卖通,独立站,LAZADA,其他 主要销售地区 非洲,欧洲,南美,东南亚,北美,东北亚,中东 有可授权的自有品牌 是 是否跨境出口专供货源, and please just tell me the english brand name only",
  max_tokens=300,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
ret = response.choices[0]['text'].strip()
print (ret)
prompt ="please extract the clean brand name from this text: %s"%ret
print (prompt)
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=prompt,
  max_tokens=300,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)
print (response.choices[0]['text'].strip())
