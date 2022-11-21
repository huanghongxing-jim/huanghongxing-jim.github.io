Jekyll::Hooks.register :documents, :post_write do 

    # copy adaptable ico images to _site dir.
    `cp $(pwd)/assets/images/favicons/* $(pwd)/_site/assets/img/favicons/`
    # copy attachments dir to _site dir.
    `cp -r $(pwd)/assets/attachments/ $(pwd)/_site/assets/`

  end