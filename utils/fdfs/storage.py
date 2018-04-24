from django.core.files.storage import FileSystemStorage
from fdfs_client.client import Fdfs_client


class FdfsStorage(FileSystemStorage):
    """自定义文件储存类"""

    def _save(self, name, content):
        """
        当用户通过django管理后台上传文件时,
        django会调用此方法来保存用户上传的文件,
        我们可以重写此方法， 把文件上传到FastDFS服务器
        :param name:
        :param content: 内容 字节类型
        :return: 返回一个path给数据库
        默认返回：return super()._save(name, content)
        """
        # 连接fdfs
        client = Fdfs_client('utils/fdfs/client.conf')
        print(111)
        try:
            # 获取内容
            datas = content.read()
            # 保存图片 返回一个json
            result = client.upload_by_buffer(datas)
            status = result.get('Status')
            # 判断返回json中的status是否为success
            if 'Upload successed.' != status:
                raise Exception('上传文件到FaseDFS失败，status为{}'.format(status))
            path = result.get('Remote file_id')
        except Exception as e:
            print(e)
            raise e

        return path

    def url(self, name):
        return 'http://127.0.0.1:8888/' + super().url(name)
