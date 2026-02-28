# 🏦 保險客戶管理系統 (Insurance CRM)

> 作者：智禾特助 🦞  
> 版本：1.0.0

## 📌 簡介

專為保險業務員設計的客戶管理系統，支援壽險與車險客戶資料管理、服務記錄追蹤、續保提醒等功能。

## ✨ 功能特色

### 客戶管理
- ✅ 新增/查詢/修改/刪除客戶資料
- ✅ 客戶分類（潛力/一般/重要/VIP）
- ✅ 匯入/匯出 CSV 格式

### 壽險管理
- ✅ 保單資料維護
- ✅ 續保到期提醒（30天內）

### 車險管理
- ✅ 強制險 + 任意險資料
- ✅ 續保到期提醒（45天內）

### 服務記錄
- ✅ 服務類型追蹤
- ✅ 服務歷史查詢

### 自動化
- ✅ 續保提醒訊息範本
- ✅ 生日祝福訊息範本

## 🚀 安裝與使用

### 環境需求
- Python 3.7+

### 安裝
```bash
# Clone 後直接執行
cd insurance-crm
python insurance_crm.py
```

### 快速操作指南

```
1. 新增客戶 - 輸入基本資料
2. 新增壽險 - 輸入保單資訊
3. 新增車險 - 輸入車險資訊
4. 匯出 CSV - 備份客戶資料
5. 匯入 CSV - 快速匯入大量客戶
```

## 📊 資料結構

### 客戶欄位
| 欄位 | 說明 |
|------|------|
| customer_id | 客戶編號 (C001) |
| name | 姓名 |
| phone | 電話 |
| email | Email |
| line_id | LINE ID |
| birthday | 出生日期 |
| customer_category | 客戶分類 |

### 壽險欄位
| 欄位 | 說明 |
|------|------|
| policy_number | 保單編號 |
| company | 保險公司 |
| product | 商品類型 |
| expiry_date | 到期日 |
| premium | 保費 |

### 車險欄位
| 欄位 | 說明 |
|------|------|
| license_plate | 車牌號碼 |
| vehicle | 車輛資訊 |
| compulsory_expiry | 強制險到期 |
| tpci | 第三人責任險 |
| vehicle_damage | 車體損失險 |

## 📁 檔案說明

```
insurance-crm/
├── insurance_crm.py    # 主程式
├── README.md           # 說明文件
├── customers.json      # 客戶資料庫
└── services.json       # 服務記錄庫
```

## 📝 License

MIT License

---

*🏦 讓保險業務更輕鬆！*
*智禾特助 🦞*
