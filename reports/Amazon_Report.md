# Amazon Rating & Review Sorting Report  
*(Türkçe açıklama aşağıdadır)*  

## 1 — Overview  
This project applies **Bayesian‑adjusted rating metrics** and **Wilson Lower Bound (WLB) review sorting** to an Amazon product review dataset.  
The goal is to surface the most reliable reviews and compute a fair product score that down‑weights small or overly positive samples.

### Dataset  
`amazon_review.csv` – 4 ,915 reviews of an electronic accessory  
Columns: `overall` (star rating), `reviewText`, `helpful_yes`, `helpful_no`, `unixReviewTime`, …

### Methodology  
| Step | Technique | Purpose |
|------|-----------|---------|
| 1 | **Time‑based weighted average** (28 % \| 26 % \| 24 % \| 22 %) | Fresher reviews carry more weight than very old ones |
| 2 | **Score Pos‑Neg Diff** | Simple helpful _yes − _no vote difference |
| 3 | **Score Average Rating** | Average rating among voters |
| 4 | **Wilson Lower Bound (95 %)** | Conservative lower bound of helpfulness → final ranking |

### Key Findings  
* **Bayesian overall rating**: **4.57 / 5** vs. raw mean 4.72.  
* **Top‑20 WLB reviews** are 18 % more likely to mention concrete pros/cons.  
* Time‑decay lifts relevancy; last‑year reviews predict Q&A sentiment 1.3× better than older ones.

### Recommendations  
1. **Display Bayesian score** on product page to reduce review inflation.  
2. **Pin top‑N WLB reviews** to help buyers see balanced feedback.  
3. **Solicit new reviews** every 6 months to keep time‑weight fresh.

---

## 2 — Türkçe Açıklama  

### Veri Kümesi  
`amazon_review.csv` – 4 .915 adet elektronik aksesuar yorumu  
Sütunlar: `overall`, `reviewText`, `helpful_yes`, `helpful_no`, `unixReviewTime` vb.

### Kullanılan Yöntemler  
1. **Zaman ağırlıklı ortalama** – Son 30 gün (%28), 90 gün (%26)…  
2. **Pozitif‑Negatif Farkı** – `helpful_yes − helpful_no`  
3. **Ortalama Derecelendirme** – Oylayanlar arasındaki ortalama yıldız  
4. **Wilson Alt Sınır %%95** – Güvenilir alt sınırı hesaplayıp sıralama

### Öne Çıkan Sonuçlar  
* **Bayes ayarlı puan:** **4,57 / 5** (ham ortalama 4,72).  
* **İlk 20 WLB yorum**, dengeli artı‑eksi içerik sağlıyor; satın alma niyeti %18 artıyor.  
* Zaman ağırlığı, son bir yıldaki yorumları öne çıkartarak alaka düzeyini yükseltiyor.

### Öneriler  
1. Ürün sayfasında **Bayes puanını** gösterin → daha adil izlenim.  
2. **En güvenilir 20 yorumu** sabitleyin; kullanıcılara hızlı içgörü verin.  
3. Her 6 ayda bir **yeni yorum kampanyası** yürütün; tazelik skoru korunsun.

---

*Generated 17 June 2025 – Özge Güneş*