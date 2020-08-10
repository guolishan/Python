import json

import requests


def login_k3c():
    k3c_headers = {
    }
    k3c_data = {
        'acctID': '5e3be3c81b92da',
        'username':'MESERP',
        'password':'wanbang2020',
        'lcid':'2052'
    }
    k3c_url = "https://k3c.wbtz.cloud/k3cloud/Kingdee.BOS.WebApi.ServicesStub.AuthService.ValidateUser.common.kdsvc"
    # 登录
    query_res = requests.post(k3c_url, data=k3c_data, headers=k3c_headers)
    headers = query_res.headers
    header_arr = str(headers['Set-Cookie']).split('path=/')
    return header_arr[0] + 'path=/'

def query_k3c_sal(tmp_cookie):
    k3c_headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{tmp_cookie}'
    }
    data_json = json.dumps({
        "data": {
            "FormId": "SAL_DELIVERYNOTICE",
            "FieldKeys": "FID,FBillNo,F_WB_SHDZ",
            "FilterString": "FSaleorgId =127414  AND FApproveDate >= '2020-07-13T00:00:00'",
            "OrderString": "",
            "TopRowCount": 0,
            "StartRow": 0,
            "Limit": 0
        }
    })
    k3c_url = "https://k3c.wbtz.cloud/k3cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"
    query_res = requests.post(k3c_url, data=data_json, headers=k3c_headers)
    return eval(query_res.text)


if __name__ == '__main__':
    k3c_cookie = login_k3c()
    query_k3c_sal(k3c_cookie)