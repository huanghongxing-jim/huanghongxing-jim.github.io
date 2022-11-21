Huang Hongxing's Blog.

> To Learn more, to recorder more!


**todo:**
1. 制作工具一键添加`{% raw %}`和`{% endraw %}`到代码块上下部分，`{{ }}`和`{% %}`中。
2. 如果使用`<name>`，build是会报错。


**写博客的命令：**

* `bundle exec jekyll b` ==> 在`linux（wsl）`下build本地博客网站的文件夹。
* `bundle exec jekyll s` ==> build完并在本地开启服务器。
* `bundle exec htmlproofer _site --disable-external --check-html --allow_hash_href` ==> 检测所build成的网页格式是否正确。
* `_plugins/post-cmd-hhx.rb`用于网站build完生成后执行的命令，博文在`_posts`文件夹写，`assets`文件夹里存放图片和附件，`post-cmd-hhx.rb`会自动在网站生成后将`assets`里的图片和附件放到`_site`正确的地方。
* `_site`目录是生成的，在`_post`里写完博文后，使用`bundle exec jekyll b`生成整个博客网站，但`_site`文件夹不用上传到github，而是通过`.github/workflows/pages-deploy.yml`在github服务器进行网站部署。
* `tools/`是一些列写博文的工具，譬如添加`{% raw %}`和`{% endraw %}`。
  

My blog is based on `jekyll-theme-chirpy`.

