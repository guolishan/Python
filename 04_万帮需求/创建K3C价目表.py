import json

import requests

global k3c_url_login,k3c_url_save,k3c_url_commit,k3c_url_audit,k3c_url_search

# K3C 登入
k3c_url_login = "http://lyqtest.wbtz.cloud/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.AuthService.ValidateUser.common.kdsvc"
# K3C 保存
k3c_url_save = "http://lyqtest.wbtz.cloud/k3cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Save.common.kdsvc"
# K3C 提交
k3c_url_commit = "http://lyqtest.wbtz.cloud/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Submit.common.kdsvc"
# K3C 审核
k3c_url_audit = "http://lyqtest.wbtz.cloud/K3Cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.Audit.common.kdsvc"
# K3C 查询
k3c_url_querry = "http://lyqtest.wbtz.cloud/k3cloud/Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"



def login_k3c():
    global k3c_url_login

    k3c_headers = {
    }

    k3c_data = {
        'acctID': '5e1eddaa26a488',
        'username':'沈逸鹏',
        'password':'888888a',
        'lcid':'2052'
    }

    # 登录
    query_res = requests.post(k3c_url_login, data=k3c_data, headers=k3c_headers)
    headers = query_res.headers
    header_arr = str(headers['Set-Cookie']).split('path=/')
    return header_arr[0] + 'path=/'


def query_k3c(tmp_cookie):
    global k3c_url_save, k3c_url_commit, k3c_url_audit, k3c_url_querry
    k3c_headers = {
        'Content-Type': 'application/json',
        'Cookie': f'{tmp_cookie}'
    }

    data_json = json.dumps({
        "formid": "PUR_PriceCategory",

        "data": {
    "Creator": "",
    "NeedUpDateFields": [],
    "NeedReturnFields": [],
    "IsDeleteEntry": "true",
    "SubSystemId": "",
    "IsVerifyBaseDataField": "false",
    "IsEntryBatchFill": "true",
    "ValidateFlag": "true",
    "NumberSearch": "true",
    "InterationFlags": "",
    "IsAutoSubmitAndAudit": "false",
    "Model": {
        "FID": 0,
        "FCreateOrgId": {
            "FNumber": "101"
        },
        "FNumber": "",
        "FName": "采购价目表测试",
        "FPriceObject": "按物料",
        "FPriceType": "采购",
        "FCurrencyID": {
            "FNumber": "PRE001"
        },
        "FSupplierID": {
            "FNumber": "32040052"
        },
        "FPricer": {},
        "FIsIncludedTax": "true",
        "FDefPriceListId": "false",
        "FDescription": "",
        "FIsPriceExcludeTax": "true",
        "F_WB_JHZQ": 0,
        "F_WB_XYDW3": {
            "FNUMBER": ""
        },
        "F_WB_XYDW2": {
            "FNUMBER": ""
        },
        "F_WB_XYDW1": {
            "FNUMBER": ""
        },
        "F_WB_JHZQ3": 0,
        "F_WB_JHZQ2": 0,
        "F_WB_JHZQ1": 0,
        "F_WB_XJDDH": "127",
        "F_WB_FXSL": 0,
        "FPriceListEntry": [
            {
                "FEntryID": 0,
                "FMaterialId": {
                    "FNumber": "ADQAMT0018"
                },
                "FAuxPropId": {},
                "FMaterialTypeId": {
                    "FNumber": ""
                },
                "FUnitID": {
                    "FNumber": "Pcs"
                },
                "FFROMQTY": 0,
                "FToQty": 0,
                "FPrice": 33,
                "FTaxPrice": 113,
                "FPublicWastePrice": 0,
                "FPublicWasteTaxPrice": 0,
                "FWastePrice": 0,
                "FWasteTaxPrice": 0,
                "FTaxRate": 13,
                "FPriceCoefficient": 0,
                "FDownPrice": 1,
                "FUpPrice": 1000,
                "FEntryEffectiveDate": "2020-08-19",
                "FEntryExpiryDate": "2020-08-30",
                "FDisablerId": {
                    "FUserID": ""
                },
                "FDisableDate": "1900-01-01",
                "FProcessOrgId": {
                    "FNumber": ""
                },
                "FPROCESSID": {
                    "FNUMBER": ""
                },
                "FDefBaseDataO": {
                    "FNUMBER": ""
                },
                "FDefBaseDataT": {
                    "FNUMBER": ""
                },
                "FDefAssistantO": {
                    "FNumber": ""
                },
                "FDefAssistantT": {
                    "FNumber": ""
                },
                "FDefTextO": "",
                "FDefTextT": "",
                "FDefaultPriceO": 0,
                "FDefaultPriceT": 0,
                "FNote": "",
                "FPRICEFROM": "",
                "FFROMBILLNO": "",
                "F_WB_XYDWDJ1": 0,
                "F_WB_XYDWDJ2": 0,
                "F_WB_XYDWDJ3": 0,
                # "F_WB_CGZQ": 15,
                # "F_WB_ZXQDL": 1,
                # "F_WB_ZXBZL": 1
            }
        ]
    }
}
    })

    query_res = requests.post(k3c_url_save, data=data_json, headers=k3c_headers)
    print(query_res.text)

    return json.dumps(query_res.text)

if __name__ == '__main__':
    k3c_cookie = login_k3c()
    text = query_k3c(k3c_cookie)

    print(text)