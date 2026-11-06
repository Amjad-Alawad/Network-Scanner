# 🌐 AMJD ALAWAD — Network Scanner

**Windows Local Area Network (LAN) Scanner**

[العربية](#-العربية) | [Türkçe](#-türkçe) | [English](#-english)

---

# 🇸🇦 العربية

## 📌 نبذة عن المشروع

**AMJD ALAWAD Network Scanner** هي أداة لفحص الشبكات المحلية (LAN) تعمل على نظام Windows، ومكتوبة بلغة Python.

تساعد الأداة على اكتشاف الأجهزة المتصلة بالشبكة المحلية، وجمع معلومات عنها، وفحص مجموعة من منافذ TCP المعروفة، وعرض النتائج بطريقة منظمة من خلال واجهة سطر الأوامر (CMD).

صُممت الأداة لتكون خفيفة وسهلة الاستخدام، ولا تحتاج إلى مكتبات خارجية لإجراء عمليات الفحص الأساسية.

## ✨ المميزات

- 🔍 اكتشاف الأجهزة المتصلة بالشبكة المحلية.
- 🌐 فحص نطاق عناوين IPv4.
- 📡 استخدام Ping للتحقق من استجابة الأجهزة.
- 🖥️ استخراج أسماء الأجهزة (Hostname) عند توفرها.
- 🔎 قراءة معلومات ARP المتاحة.
- 🏷️ محاولة تحديد الشركة المصنعة لبطاقة الشبكة من عنوان MAC.
- 🔌 فحص مجموعة من منافذ TCP الشائعة.
- 📊 تصنيف الأجهزة بشكل تقريبي حسب المعلومات المتاحة.
- 💾 حفظ سجل عمليات الفحص في SQLite.
- 📁 تصدير النتائج إلى CSV وJSON.
- ⚡ تنفيذ عمليات الفحص بالتوازي لتحسين السرعة.
- 🖥️ واجهة استخدام من خلال CMD.

## 🛠️ المتطلبات

- Windows 10 أو Windows 11.
- Python 3.11 أو أحدث.
- Git (اختياري).
- اتصال بالشبكة المحلية.

لا تحتاج عمليات الفحص الأساسية إلى تثبيت Scapy أو Npcap.

## 🚀 طريقة التشغيل

**1. تحميل المشروع**

```bash
git clone https://github.com/Amjad-Alawad/Network-Scanner.git
```

**2. الدخول إلى مجلد المشروع**

```bash
cd Network-Scanner
```

**3. تشغيل الأداة**

```bash
python amjd_lan_scanner.py
```

## 🌐 مثال على نطاق الشبكة

إذا كان عنوان جهازك:

```text
192.168.1.8
```

وكان قناع الشبكة:

```text
255.255.255.0
```

فإن نطاق الشبكة هو:

```text
192.168.1.0/24
```

يمكن استخدام هذا النطاق لفحص الأجهزة الموجودة على الشبكة المحلية.

## 🔌 المنافذ التي يمكن فحصها

تتضمن قائمة المنافذ الافتراضية:

| Port | Service |
|---:|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 53 | DNS |
| 80 | HTTP |
| 135 | MS RPC |
| 139 | NetBIOS |
| 443 | HTTPS |
| 445 | SMB |
| 554 | RTSP |
| 631 | IPP |
| 3389 | RDP |
| 8080 | HTTP Alternative |
| 8443 | HTTPS Alternative |
| 9100 | Printer |

## 📂 تصدير النتائج

تدعم الأداة تصدير نتائج الفحص بصيغتين:

- **CSV:** لفتح النتائج وتحليلها باستخدام Excel.
- **JSON:** لاستخدام النتائج مع برامج وأدوات أخرى.

كما يتم حفظ سجل عمليات الفحص في قاعدة بيانات SQLite.

## ⚠️ ملاحظات تقنية

- لا يمكن ضمان اكتشاف جميع الأجهزة؛ بعض الأجهزة تمنع ICMP Ping.
- يعتمد اكتشاف عناوين MAC على المعلومات المتاحة في ARP Cache.
- قد لا تظهر معلومات الشركة المصنعة إذا تعذر الحصول على عنوان MAC أو لم تتوفر بيانات OUI.
- فحص المنافذ يقتصر على المنافذ المحددة داخل الأداة.
- تصنيف نوع الجهاز تقديري وليس تحديداً مؤكداً.
- الشبكات الافتراضية مثل VirtualBox قد تظهر كواجهات منفصلة.
- قد تؤثر إعدادات الجدار الناري وعزل الأجهزة في نتائج الفحص.

## 🔐 الاستخدام المسؤول

هذا المشروع مخصص للتعلم وإدارة الشبكات وفحص الشبكات التي تملكها أو لديك تصريح صريح بفحصها.

لا تستخدم الأداة لفحص شبكات أو أجهزة دون إذن أصحابها.

## 👨‍💻 المطور

**AMJD ALAWAD**

GitHub: https://github.com/Amjad-Alawad

---

# 🇹🇷 Türkçe

## 📌 Proje Hakkında

**AMJD ALAWAD Network Scanner**, Windows işletim sistemi üzerinde çalışan ve Python ile geliştirilmiş bir yerel ağ tarama aracıdır.

Bu araç, yerel ağa bağlı cihazları keşfetmek, cihazlar hakkında mevcut bilgileri toplamak ve belirli TCP portlarını kontrol etmek için tasarlanmıştır.

Tarama sonuçları CMD (Komut İstemi) üzerinden görüntülenebilir.

## ✨ Özellikler

- 🔍 Yerel ağa bağlı cihazları keşfetme.
- 🌐 IPv4 ağ aralığını tarama.
- 📡 Ping ile cihazların yanıt durumunu kontrol etme.
- 🖥️ Hostname bilgilerini çözümleme.
- 🔎 ARP tablosundaki mevcut bilgileri okuma.
- 🏷️ MAC adresinden üretici bilgisi belirlemeye çalışma.
- 🔌 Yaygın TCP portlarını tarama.
- 📊 Cihazları tahmini olarak sınıflandırma.
- 💾 Tarama geçmişini SQLite veritabanında saklama.
- 📁 Sonuçları CSV ve JSON formatlarında dışa aktarma.
- ⚡ Paralel tarama ile performansı artırma.
- 🖥️ CMD üzerinden kolay kullanım.

## 🛠️ Gereksinimler

- Windows 10 veya Windows 11.
- Python 3.11 veya üzeri.
- Git (isteğe bağlı).
- Yerel ağ bağlantısı.

Temel tarama işlemleri için Scapy veya Npcap kurulumu gerekmez.

## 🚀 Kurulum ve Çalıştırma

**1. Projeyi indirin**

```bash
git clone https://github.com/Amjad-Alawad/Network-Scanner.git
```

**2. Proje klasörüne girin**

```bash
cd Network-Scanner
```

**3. Programı çalıştırın**

```bash
python amjd_lan_scanner.py
```

## 🌐 Ağ Aralığı Örneği

Bilgisayarınızın IP adresi:

```text
192.168.1.8
```

Alt ağ maskesi:

```text
255.255.255.0
```

Ağ aralığı:

```text
192.168.1.0/24
```

Bu aralık, yerel ağdaki cihazları taramak için kullanılabilir.

## 🔌 Taranan TCP Portları

| Port | Servis |
|---:|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 53 | DNS |
| 80 | HTTP |
| 135 | MS RPC |
| 139 | NetBIOS |
| 443 | HTTPS |
| 445 | SMB |
| 554 | RTSP |
| 631 | IPP |
| 3389 | RDP |
| 8080 | HTTP Alternative |
| 8443 | HTTPS Alternative |
| 9100 | Printer |

## 📂 Sonuçların Dışa Aktarılması

Tarama sonuçları iki farklı formatta dışa aktarılabilir:

- **CSV:** Excel ile açılabilir ve analiz edilebilir.
- **JSON:** Diğer yazılımlar ve araçlarla kullanılabilir.

Tarama geçmişi SQLite veritabanında saklanır.

## ⚠️ Teknik Notlar

- ICMP Ping engellenmişse bazı cihazlar tespit edilemeyebilir.
- MAC adresleri ARP önbelleğinde bulunan bilgilere bağlıdır.
- OUI verisi bulunamazsa üretici bilgisi gösterilemeyebilir.
- Port taraması yalnızca tanımlı portlarla sınırlıdır.
- Cihaz türü sınıflandırması tahminidir.
- VirtualBox gibi sanal ağ adaptörleri ayrı ağ arayüzleri olarak görünebilir.
- Güvenlik duvarı ve istemci izolasyonu sonuçları etkileyebilir.

## 🔐 Sorumlu Kullanım

Bu proje eğitim, ağ yönetimi ve yalnızca sahibi olduğunuz veya tarama izniniz bulunan ağlarda kullanım amacıyla geliştirilmiştir.

İzinsiz ağ veya cihaz taraması yapmayın.

## 👨‍💻 Geliştirici

**AMJD ALAWAD**

GitHub: https://github.com/Amjad-Alawad

---

# 🇬🇧 English

## 📌 About the Project

**AMJD ALAWAD Network Scanner** is a Python-based Local Area Network (LAN) scanning tool designed for Windows.

It helps discover devices connected to a local network, collect available device information, and check a selected list of common TCP ports.

Scan results are displayed through a Command Prompt (CMD) interface.

The core scanning functionality uses Python's standard library and native Windows networking commands.

## ✨ Features

- 🔍 Local network device discovery.
- 🌐 IPv4 subnet scanning.
- 📡 Ping-based host availability checks.
- 🖥️ Hostname resolution.
- 🔎 ARP cache inspection.
- 🏷️ MAC vendor identification when OUI data is available.
- 🔌 Common TCP port scanning.
- 📊 Heuristic device classification.
- 💾 SQLite scan history.
- 📁 CSV and JSON report exports.
- ⚡ Concurrent scanning for improved performance.
- 🖥️ Command-line interface.

## 🛠️ Requirements

- Windows 10 or Windows 11.
- Python 3.11 or newer.
- Git (optional).
- Local network connectivity.

Scapy and Npcap are not required for the core scanning functionality.

## 🚀 Installation and Usage

**1. Clone the repository**

```bash
git clone https://github.com/Amjad-Alawad/Network-Scanner.git
```

**2. Open the project directory**

```bash
cd Network-Scanner
```

**3. Run the scanner**

```bash
python amjd_lan_scanner.py
```

## 🌐 Network Range Example

Computer IPv4 address:

```text
192.168.1.8
```

Subnet mask:

```text
255.255.255.0
```

Network CIDR:

```text
192.168.1.0/24
```

Use this CIDR range to scan devices on the local network.

## 🔌 TCP Ports Scanned

The default port list includes:

| Port | Service |
|---:|---|
| 21 | FTP |
| 22 | SSH |
| 23 | Telnet |
| 53 | DNS |
| 80 | HTTP |
| 135 | MS RPC |
| 139 | NetBIOS |
| 443 | HTTPS |
| 445 | SMB |
| 554 | RTSP |
| 631 | IPP |
| 3389 | RDP |
| 8080 | HTTP Alternative |
| 8443 | HTTPS Alternative |
| 9100 | Printer |

## 📂 Exporting Scan Results

The scanner supports two export formats:

- **CSV:** Suitable for Microsoft Excel and spreadsheet analysis.
- **JSON:** Suitable for integration with other applications and scripts.

Scan history is stored in a local SQLite database.

## ⚠️ Technical Limitations

- Devices that block ICMP Ping may not be discovered.
- MAC address discovery depends on available ARP cache entries.
- Vendor identification may be unavailable when MAC or OUI information is missing.
- Port scanning is limited to the configured port list.
- Device classification is heuristic and may not always be accurate.
- Virtual network adapters, including VirtualBox adapters, may appear as separate interfaces.
- Firewalls and client isolation can affect scan results.

## 🔐 Responsible Use

This project is intended for educational purposes, network administration, and scanning networks that you own or have explicit permission to test.

Do not scan networks or devices without authorization.

## 👨‍💻 Developer

**AMJD ALAWAD**

GitHub: https://github.com/Amjad-Alawad

---

## 📜 License

This project is distributed under the MIT License.

See the `LICENSE` file for details.

---

**AMJD ALAWAD — Network Scanner**  
*Discover. Scan. Analyze.*
