# 保險客戶管理系統 (Insurance CRM)
# 作者: 智禾特助 🦞
# 版本: 1.0.0

import json
import os
from datetime import datetime, timedelta
from typing import Optional
import csv

# 資料檔案路徑
DATA_FILE = "customers.json"
SERVICE_FILE = "services.json"

class InsuranceCRM:
    """保險客戶管理系統"""
    
    def __init__(self):
        self.customers = self.load_data(DATA_FILE)
        self.services = self.load_data(SERVICE_FILE)
    
    def load_data(self, filename: str) -> dict:
        """載入資料"""
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def save_data(self, filename: str, data: dict):
        """儲存資料"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ========== 客戶資料操作 ==========
    
    def add_customer(self, customer_data: dict) -> str:
        """新增客戶"""
        # 自動產生客戶編號
        max_id = 0
        for cid in self.customers.keys():
            if cid.startswith('C'):
                try:
                    num = int(cid[1:])
                    max_id = max(max_id, num)
                except:
                    pass
        customer_id = f"C{max_id + 1:03d}"
        
        customer_data['customer_id'] = customer_id
        customer_data['created_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        customer_data['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.customers[customer_id] = customer_data
        self.save_data(DATA_FILE, self.customers)
        return customer_id
    
    def get_customer(self, customer_id: str) -> Optional[dict]:
        """查詢客戶"""
        return self.customers.get(customer_id)
    
    def list_customers(self, category: str = None) -> list:
        """列出所有客戶"""
        customers = list(self.customers.values())
        if category:
            customers = [c for c in customers if c.get('customer_category') == category]
        return customers
    
    def update_customer(self, customer_id: str, updates: dict) -> bool:
        """更新客戶資料"""
        if customer_id in self.customers:
            updates['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.customers[customer_id].update(updates)
            self.save_data(DATA_FILE, self.customers)
            return True
        return False
    
    def delete_customer(self, customer_id: str) -> bool:
        """刪除客戶"""
        if customer_id in self.customers:
            del self.customers[customer_id]
            self.save_data(DATA_FILE, self.customers)
            # 同時刪除相關服務記錄
            self.services = {k: v for k, v in self.services.items() 
                            if v.get('customer_id') != customer_id}
            self.save_data(SERVICE_FILE, self.services)
            return True
        return False
    
    # ========== 壽險操作 ==========
    
    def add_life_insurance(self, customer_id: str, life_data: dict) -> bool:
        """新增壽險資料"""
        if customer_id in self.customers:
            if 'life_insurance' not in self.customers[customer_id]:
                self.customers[customer_id]['life_insurance'] = []
            self.customers[customer_id]['life_insurance'].append(life_data)
            self.save_data(DATA_FILE, self.customers)
            return True
        return False
    
    def get_life_insurance_expiring(self, days: int = 30) -> list:
        """取得即將到期的壽險"""
        expiring = []
        today = datetime.now()
        for customer in self.customers.values():
            if 'life_insurance' in customer:
                for life in customer['life_insurance']:
                    if life.get('expiry_date'):
                        try:
                            expiry = datetime.strptime(life['expiry_date'], "%Y-%m-%d")
                            if 0 <= (expiry - today).days <= days:
                                expiring.append({
                                    'customer_id': customer['customer_id'],
                                    'customer_name': customer.get('name', ''),
                                    'phone': customer.get('phone', ''),
                                    'policy_number': life.get('policy_number', ''),
                                    'expiry_date': life['expiry_date'],
                                    'premium': life.get('premium', ''),
                                    'company': life.get('company', '')
                                })
                        except:
                            pass
        return expiring
    
    # ========== 車險操作 ==========
    
    def add_auto_insurance(self, customer_id: str, auto_data: dict) -> bool:
        """新增車險資料"""
        if customer_id in self.customers:
            if 'auto_insurance' not in self.customers[customer_id]:
                self.customers[customer_id]['auto_insurance'] = []
            self.customers[customer_id]['auto_insurance'].append(auto_data)
            self.save_data(DATA_FILE, self.customers)
            return True
        return False
    
    def get_auto_insurance_expiring(self, days: int = 45) -> list:
        """取得即將到期的車險"""
        expiring = []
        today = datetime.now()
        for customer in self.customers.values():
            if 'auto_insurance' in customer:
                for auto in customer['auto_insurance']:
                    if auto.get('compulsory_expiry'):
                        try:
                            expiry = datetime.strptime(auto['compulsory_expiry'], "%Y-%m-%d")
                            if 0 <= (expiry - today).days <= days:
                                expiring.append({
                                    'customer_id': customer['customer_id'],
                                    'customer_name': customer.get('name', ''),
                                    'phone': customer.get('phone', ''),
                                    'license_plate': auto.get('license_plate', ''),
                                    'vehicle': auto.get('vehicle', ''),
                                    'expiry_date': auto['compulsory_expiry'],
                                    'premium': auto.get('compulsory_premium', ''),
                                    'company': auto.get('compulsory_company', '')
                                })
                        except:
                            pass
        return expiring
    
    # ========== 服務記錄操作 ==========
    
    def add_service(self, customer_id: str, service_data: dict) -> bool:
        """新增服務記錄"""
        if customer_id not in self.customers:
            return False
        
        service_id = f"S{len(self.services) + 1:04d}"
        service_data['service_id'] = service_id
        service_data['customer_id'] = customer_id
        service_data['service_date'] = datetime.now().strftime("%Y-%m-%d")
        
        self.services[service_id] = service_data
        self.save_data(SERVICE_FILE, self.services)
        return True
    
    def get_customer_services(self, customer_id: str) -> list:
        """取得客戶服務記錄"""
        return [s for s in self.services.values() 
                if s.get('customer_id') == customer_id]
    
    # ========== 匯入匯出 ==========
    
    def export_to_csv(self, filename: str = "customers_export.csv"):
        """匯出客戶資料到 CSV"""
        if not self.customers:
            print("沒有客戶資料可匯出")
            return
        
        # 定義 CSV 欄位
        fields = [
            'customer_id', 'name', 'title', 'phone', 'email', 'line_id',
            'birthday', 'first_insurance_date', 'customer_category', 'remark',
            'life_policy_number', 'life_company', 'life_product', 'life_date',
            'life_expiry', 'life_premium', 'life_coverage', 'life_sales',
            'auto_license_plate', 'auto_brand', 'auto_model', 'auto_cc',
            'auto_compulsory_company', 'auto_compulsory_date', 'auto_compulsory_expiry',
            'auto_compulsory_premium', 'auto_tpci', 'auto_tpci_coverage', 'auto_tpci_premium',
            'auto_vehicle_damage', 'auto_vehicle_coverage', 'auto_vehicle_premium',
            'auto_passenger', 'auto_passenger_coverage', 'auto_passenger_premium',
            'auto_deductible', 'auto_deductible_premium'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
            writer.writeheader()
            
            for customer in self.customers.values():
                row = {
                    'customer_id': customer.get('customer_id', ''),
                    'name': customer.get('name', ''),
                    'title': customer.get('title', ''),
                    'phone': customer.get('phone', ''),
                    'email': customer.get('email', ''),
                    'line_id': customer.get('line_id', ''),
                    'birthday': customer.get('birthday', ''),
                    'first_insurance_date': customer.get('first_insurance_date', ''),
                    'customer_category': customer.get('customer_category', ''),
                    'remark': customer.get('remark', '')
                }
                
                # 壽險資料
                if 'life_insurance' in customer and customer['life_insurance']:
                    life = customer['life_insurance'][0]
                    row.update({
                        'life_policy_number': life.get('policy_number', ''),
                        'life_company': life.get('company', ''),
                        'life_product': life.get('product', ''),
                        'life_date': life.get('insurance_date', ''),
                        'life_expiry': life.get('expiry_date', ''),
                        'life_premium': life.get('premium', ''),
                        'life_coverage': life.get('coverage', ''),
                        'life_sales': life.get('salesperson', '')
                    })
                
                # 車險資料
                if 'auto_insurance' in customer and customer['auto_insurance']:
                    auto = customer['auto_insurance'][0]
                    row.update({
                        'auto_license_plate': auto.get('license_plate', ''),
                        'auto_brand': auto.get('brand', ''),
                        'auto_model': auto.get('model', ''),
                        'auto_cc': auto.get('displacement', ''),
                        'auto_compulsory_company': auto.get('compulsory_company', ''),
                        'auto_compulsory_date': auto.get('compulsory_date', ''),
                        'auto_compulsory_expiry': auto.get('compulsory_expiry', ''),
                        'auto_compulsory_premium': auto.get('compulsory_premium', ''),
                        'auto_tpci': auto.get('tpci', ''),
                        'auto_tpci_coverage': auto.get('tpci_coverage', ''),
                        'auto_tpci_premium': auto.get('tpci_premium', ''),
                        'auto_vehicle_damage': auto.get('vehicle_damage', ''),
                        'auto_vehicle_coverage': auto.get('vehicle_coverage', ''),
                        'auto_vehicle_premium': auto.get('vehicle_premium', ''),
                        'auto_passenger': auto.get('passenger', ''),
                        'auto_passenger_coverage': auto.get('passenger_coverage', ''),
                        'auto_passenger_premium': auto.get('passenger_premium', ''),
                        'auto_deductible': auto.get('deductible', ''),
                        'auto_deductible_premium': auto.get('deductible_premium', '')
                    })
                
                writer.writerow(row)
        
        print(f"已匯出 {len(self.customers)} 筆客戶資料到 {filename}")
    
    def import_from_csv(self, filename: str) -> int:
        """從 CSV 匯入客戶資料"""
        imported = 0
        with open(filename, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                customer_data = {
                    'name': row.get('name', ''),
                    'title': row.get('title', ''),
                    'phone': row.get('phone', ''),
                    'email': row.get('email', ''),
                    'line_id': row.get('line_id', ''),
                    'birthday': row.get('birthday', ''),
                    'first_insurance_date': row.get('first_insurance_date', ''),
                    'customer_category': row.get('customer_category', ''),
                    'remark': row.get('remark', '')
                }
                
                # 壽險資料
                if row.get('life_policy_number'):
                    customer_data['life_insurance'] = [{
                        'policy_number': row.get('life_policy_number', ''),
                        'company': row.get('life_company', ''),
                        'product': row.get('life_product', ''),
                        'insurance_date': row.get('life_date', ''),
                        'expiry_date': row.get('life_expiry', ''),
                        'premium': row.get('life_premium', ''),
                        'coverage': row.get('life_coverage', ''),
                        'salesperson': row.get('life_sales', '')
                    }]
                
                # 車險資料
                if row.get('auto_license_plate'):
                    customer_data['auto_insurance'] = [{
                        'license_plate': row.get('auto_license_plate', ''),
                        'brand': row.get('auto_brand', ''),
                        'model': row.get('auto_model', ''),
                        'displacement': row.get('auto_cc', ''),
                        'compulsory_company': row.get('auto_compulsory_company', ''),
                        'compulsory_date': row.get('auto_compulsory_date', ''),
                        'compulsory_expiry': row.get('auto_compulsory_expiry', ''),
                        'compulsory_premium': row.get('auto_compulsory_premium', ''),
                        'tpci': row.get('auto_tpci', ''),
                        'tpci_coverage': row.get('auto_tpci_coverage', ''),
                        'tpci_premium': row.get('auto_tpci_premium', ''),
                        'vehicle_damage': row.get('auto_vehicle_damage', ''),
                        'vehicle_coverage': row.get('auto_vehicle_coverage', ''),
                        'vehicle_premium': row.get('auto_vehicle_premium', ''),
                        'passenger': row.get('auto_passenger', ''),
                        'passenger_coverage': row.get('auto_passenger_coverage', ''),
                        'passenger_premium': row.get('auto_passenger_premium', ''),
                        'deductible': row.get('auto_deductible', ''),
                        'deductible_premium': row.get('auto_deductible_premium', '')
                    }]
                
                self.add_customer(customer_data)
                imported += 1
        
        print(f"已匯入 {imported} 筆客戶資料")
        return imported
    
    # ========== 統計功能 ==========
    
    def get_statistics(self) -> dict:
        """取得統計資料"""
        stats = {
            'total_customers': len(self.customers),
            'by_category': {},
            'total_life_policies': 0,
            'total_auto_policies': 0,
            'total_services': len(self.services)
        }
        
        for customer in self.customers.values():
            cat = customer.get('customer_category', '一般')
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
            
            if 'life_insurance' in customer:
                stats['total_life_policies'] += len(customer['life_insurance'])
            if 'auto_insurance' in customer:
                stats['total_auto_policies'] += len(customer['auto_insurance'])
        
        return stats
    
    # ========== 自動化訊息 ==========
    
    def generate_renewal_message(self, customer: dict, insurance_type: str) -> str:
        """產生續保提醒訊息"""
        if insurance_type == 'life':
            life = customer.get('life_insurance', [{}])[0]
            return f"""【壽險續保服務】

{customer.get('name', '您好')} 您好：

感謝您一直以來的支持！您的壽險保單即將於 {life.get('expiry_date', 'OO')} 到期，請問需要我幫您辦理續保手續嗎？

📋 保單編號：{life.get('policy_number', 'XXXXX')}
💰 壽險保費：{life.get('premium', 'XXX')} 元

另外，這一年您的家庭狀況有沒有什麼變化呢？
需要我幫您檢視保障是否足夠嗎？

期待您的回覆！
Carol 敬上"""
        
        elif insurance_type == 'auto':
            auto = customer.get('auto_insurance', [{}])[0]
            return f"""【車險續保提醒】

{customer.get('name', '您好')} 您好：

您的強制險即將於 {auto.get('compulsory_expiry', 'OO')} 到期，為確保您的保障不中斷，請問需要我幫您協助續保嗎？

🚗 車牌：{auto.get('license_plate', 'ABC-1234')}
📋 強制險到期：{auto.get('compulsory_expiry', 'OO')}
💰 強制險保費：{auto.get('compulsory_premium', '1,688')} 元

另外，這一年您的駕駛狀況如何呢？
需要我幫您評估是否有更適合的車險方案嗎？

感謝您的支持！
Carol 敬上"""
        
        return ""
    
    def generate_birthday_message(self, customer: dict) -> str:
        """產生生日祝福訊息"""
        return f"""【生日祝福】

{customer.get('name', '您好')} 您好：

🎂 生日快樂！🎂

感謝您一直以來的支持與信任，
在這特別的日子裡，祝福您：

🎉 生日快樂、身體健康、
💰 財運亨通、萬事如意！

期待繼續為您服務！

Carol 敬上"""


# ========== CLI 選單 ==========

def print_menu():
    """顯示選單"""
    print("\n" + "="*50)
    print("🏦 保險客戶管理系統 (Insurance CRM)")
    print("="*50)
    print("1. 新增客戶")
    print("2. 查詢客戶")
    print("3. 列出所有客戶")
    print("4. 更新客戶資料")
    print("5. 刪除客戶")
    print("6. 新增壽險資料")
    print("7. 新增車險資料")
    print("8. 新增服務記錄")
    print("9. 查詢服務記錄")
    print("10. 壽險續保提醒")
    print("11. 車險續保提醒")
    print("12. 匯出 CSV")
    print("13. 匯入 CSV")
    print("14. 統計資料")
    print("0. 離開系統")
    print("="*50)


def main():
    """主程式"""
    crm = InsuranceCRM()
    
    while True:
        print_menu()
        choice = input("請選擇功能 (0-14): ").strip()
        
        if choice == '0':
            print("感謝使用，再見！")
            break
        
        elif choice == '1':
            # 新增客戶
            print("\n【新增客戶】")
            customer = {
                'name': input("姓名: "),
                'title': input("稱謂 (先生/小姐/太太): "),
                'phone': input("電話: "),
                'email': input("Email: "),
                'line_id': input("LINE ID: "),
                'birthday': input("出生日期 (YYYY-MM-DD): "),
                'first_insurance_date': input("首次投保日期 (YYYY-MM-DD): "),
                'customer_category': input("客戶分類 (潛力/一般/重要/VIP): "),
                'remark': input("備註: ")
            }
            cid = crm.add_customer(customer)
            print(f"✓ 客戶新增成功！客戶編號: {cid}")
        
        elif choice == '2':
            # 查詢客戶
            print("\n【查詢客戶】")
            cid = input("請輸入客戶編號: ")
            customer = crm.get_customer(cid)
            if customer:
                print("\n--- 客戶資料 ---")
                for k, v in customer.items():
                    if k not in ['life_insurance', 'auto_insurance']:
                        print(f"{k}: {v}")
                if customer.get('life_insurance'):
                    print("\n--- 壽險資料 ---")
                    for life in customer['life_insurance']:
                        for k, v in life.items():
                            print(f"{k}: {v}")
                if customer.get('auto_insurance'):
                    print("\n--- 車險資料 ---")
                    for auto in customer['auto_insurance']:
                        for k, v in auto.items():
                            print(f"{k}: {v}")
            else:
                print("找不到客戶")
        
        elif choice == '3':
            # 列出所有客戶
            print("\n【客戶列表】")
            category = input("篩選分類 (直接Enter顯示全部): ").strip()
            customers = crm.list_customers(category if category else None)
            print(f"\n共有 {len(customers)} 位客戶:")
            for c in customers:
                print(f"  {c.get('customer_id')}: {c.get('name')} ({c.get('phone')})")
        
        elif choice == '4':
            # 更新客戶
            print("\n【更新客戶】")
            cid = input("客戶編號: ")
            field = input("欄位: ")
            value = input("新值: ")
            if crm.update_customer(cid, {field: value}):
                print("✓ 更新成功")
            else:
                print("找不到客戶")
        
        elif choice == '5':
            # 刪除客戶
            print("\n【刪除客戶】")
            cid = input("請輸入客戶編號: ")
            if crm.delete_customer(cid):
                print("✓ 刪除成功")
            else:
                print("找不到客戶")
        
        elif choice == '6':
            # 新增壽險
            print("\n【新增壽險】")
            cid = input("客戶編號: ")
            life = {
                'policy_number': input("保單編號: "),
                'company': input("保險公司: "),
                'product': input("商品 (重大疾病/壽險/醫療): "),
                'insurance_date': input("投保日期 (YYYY-MM-DD): "),
                'expiry_date': input("到期日 (YYYY-MM-DD): "),
                'premium': input("保費: "),
                'coverage': input("保障內容: "),
                'salesperson': input("業務員: ")
            }
            if crm.add_life_insurance(cid, life):
                print("✓ 壽險資料新增成功")
            else:
                print("找不到客戶")
        
        elif choice == '7':
            # 新增車險
            print("\n【新增車險】")
            cid = input("客戶編號: ")
            auto = {
                'license_plate': input("車牌號碼: "),
                'brand': input("車輛廠牌: "),
                'model': input("車輛型號: "),
                'displacement': input("排量CC數: "),
                'compulsory_company': input("強制險公司: "),
                'compulsory_date': input("強制險投保日期: "),
                'compulsory_expiry': input("強制險到期日: "),
                'compulsory_premium': input("強制險保費: "),
                'tpci': input("第三人責任險 (有/無): "),
                'tpci_coverage': input("第三人保額: "),
                'tpci_premium': input("第三人保費: "),
                'vehicle_damage': input("車體損失險 (甲式/乙式/丙式/無): "),
                'vehicle_coverage': input("車體保額: "),
                'vehicle_premium': input("車體保費: "),
                'passenger': input("乘客險 (有/無): "),
                'passenger_coverage': input("乘客險保額: "),
                'passenger_premium': input("乘客險保費: "),
                'deductible': input("車險免自負 (有/無): "),
                'deductible_premium': input("免自負保費: ")
            }
            if crm.add_auto_insurance(cid, auto):
                print("✓ 車險資料新增成功")
            else:
                print("找不到客戶")
        
        elif choice == '8':
            # 新增服務記錄
            print("\n【新增服務記錄】")
            cid = input("客戶編號: ")
            service = {
                'service_type': input("服務類型 (壽險關懷/車險理賠/變更/檢視/其他): "),
                'content': input("服務內容: "),
                'duration': input("花費時間: "),
                'next_followup': input("下次跟進日期: ")
            }
            if crm.add_service(cid, service):
                print("✓ 服務記錄新增成功")
            else:
                print("找不到客戶")
        
        elif choice == '9':
            # 查詢服務記錄
            print("\n【服務記錄查詢】")
            cid = input("客戶編號: ")
            services = crm.get_customer_services(cid)
            if services:
                for s in services:
                    print(f"\n日期: {s.get('service_date')}")
                    print(f"類型: {s.get('service_type')}")
                    print(f"內容: {s.get('content')}")
            else:
                print("沒有服務記錄")
        
        elif choice == '10':
            # 壽險續保提醒
            print("\n【壽險續保提醒 (30天內)】")
            expiring = crm.get_life_insurance_expiring(30)
            if expiring:
                for e in expiring:
                    print(f"\n客戶: {e['customer_name']} ({e['customer_id']})")
                    print(f"電話: {e['phone']}")
                    print(f"保單: {e['policy_number']}")
                    print(f"到期日: {e['expiry_date']}")
                    print(f"保費: {e['premium']}")
                    print("-" * 30)
            else:
                print("沒有即將到期的壽險")
        
        elif choice == '11':
            # 車險續保提醒
            print("\n【車險續保提醒 (45天內)】")
            expiring = crm.get_auto_insurance_expiring(45)
            if expiring:
                for e in expiring:
                    print(f"\n客戶: {e['customer_name']} ({e['customer_id']})")
                    print(f"電話: {e['phone']}")
                    print(f"車牌: {e['license_plate']}")
                    print(f"到期日: {e['expiry_date']}")
                    print(f"保費: {e['premium']}")
                    print("-" * 30)
            else:
                print("沒有即將到期的車險")
        
        elif choice == '12':
            # 匯出 CSV
            print("\n【匯出 CSV】")
            crm.export_to_csv()
        
        elif choice == '13':
            # 匯入 CSV
            print("\n【匯入 CSV】")
            filename = input("請輸入CSV檔名: ")
            crm.import_from_csv(filename)
        
        elif choice == '14':
            # 統計資料
            print("\n【統計資料】")
            stats = crm.get_statistics()
            print(f"總客戶數: {stats['total_customers']}")
            print(f"壽險保單: {stats['total_life_policies']}")
            print(f"車險保單: {stats['total_auto_policies']}")
            print(f"服務記錄: {stats['total_services']}")
            print("\n客戶分類:")
            for cat, count in stats['by_category'].items():
                print(f"  {cat}: {count}")


if __name__ == "__main__":
    main()
