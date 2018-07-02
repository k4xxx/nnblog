import re
class MyValid:

    @staticmethod
    def valid(valid_str,str_name='',not_null=True,is_loginname=False,is_alnum=False,is_digit=False,max_length=None,less_length=None,
              is_email=False,is_telephone=False):
        '''
        验证一个字符串是否符合指定规则
        :param valid_str: 需要验证的字符串
        :param str_name: 需要验证的字符串的名字
        :param not_null: 是否不为空
        :param max_length: 最大长度
        :param less_length: 最小长度
        :param is_telephone: 是否是电话号码
        :param is_email: 是否是邮箱
        :param is_qq: 是否是qq
        :param is_alnum: 是否为数字和字母组成,包括中文(用来验证昵称)
        :param is_loginname: 是否全部为英文字母和字母组成（不包括中文），并且首字母不能为数字（用来判断用户名或者路径）
        :return: 返回一个字典
        '''
        res_dic = {'state':True,'error_msg':[]}
        if not_null:
            if valid_str.strip() == '':
                res_dic['state'] = False
                res_dic['error_msg'].append('{}不能为空，请输入内容'.format(str_name))

        if is_loginname:
            if not re.match(r'[a-zA-Z0-9]+',valid_str):
                res_dic['state'] = False
                res_dic['error_msg'].append('{}必须由字母和数字组成'.format(str_name))
                print(valid_str[0],valid_str[0].isdigit())
            elif valid_str[0].isdigit():
                res_dic['state'] = False
                res_dic['error_msg'].append('{}首字母不能为数字组成.'.format(str_name))

        if is_digit:
            if not valid_str.isdigit():
                res_dic['state'] = False
                res_dic['error_msg'].append('{}必须全部由数字组成.'.format(str_name))

        if is_alnum:
            if not valid_str.isalnum():
                res_dic['state'] = False
                res_dic['error_msg'].append('{}中不能含有特殊符号.'.format(str_name))
            elif valid_str[0].isdigit():
                res_dic['state'] = False
                res_dic['error_msg'].append('{}首字母不能为数字组成.'.format(str_name))

        if max_length:
            if len(valid_str) > max_length:
                res_dic['state'] = False
                res_dic['error_msg'].append('{}最大长度不超过{}位.'.format(str_name, max_length))

        if less_length:
            if len(valid_str) < less_length:
                res_dic['state'] = False
                res_dic['error_msg'].append('{}最小长度不小于{}位.'.format(str_name, less_length))


        if is_telephone:
            if len(valid_str) != 11 or not re.match(r'[1]{1}[0-9]{10}', valid_str):
                res_dic['state'] = False
                res_dic['error_msg'].append('{}格式不正确，请重输.'.format(str_name))

        if is_email:
            if len(valid_str) < 7 or not re.match(r'^.+\@(\[?)[a-zA-Z0-9\-\.]+\.([a-zA-Z]{2,3}|[0-9]{1,3})(\]?)$', valid_str):
                res_dic['state'] = False
                res_dic['error_msg'].append('{}格式不正确，请重输.'.format(str_name))

        return res_dic


if __name__ == '__main__':
    res = MyValid.valid('a@qq.com',str_name='邮箱',is_email=True)
    print(res['state'],res['error_msg'])