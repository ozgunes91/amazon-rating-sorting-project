
###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı



###################################################
# GÖREV 1: Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslayınız.
###################################################
import pandas as pd
import math
import scipy.stats as st
from sklearn.preprocessing import MinMaxScaler

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.10f' % x)

# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır.
# Bu görevde amacımız verilen puanları tarihe göre ağırlıklandırarak değerlendirmek.
# İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın karşılaştırılması gerekmektedir.


###################################################
# Adım 1: Veri Setini Okutunuz ve Ürünün Ortalama Puanını Hesaplayınız.
###################################################

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "amazon_review.csv"
df_ = pd.read_csv(DATA_PATH)
df = df_.copy()
df.head()
df.shape # 4915 gözlem, 12 değişken var.

df.groupby("asin").agg({"overall":"mean"})
# veya
df["overall"].mean() #(4.587589013224822)
# #küsüratlı kısmı daha uzun gösteriyor.

###################################################
# Adım 2: Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
###################################################
df.head()
df.info()

df["reviewTime"] = pd.to_datetime(df["reviewTime"]) #öncelikle tipini zaman formatına çeviriyoruz.
df["reviewTime"].max() #en son tarih "2014-12-07 00:00:00" #kendim görmek istedim.
#gün değişkeni olduğundan oluşturmadık yoksa bir analiz tarihi girip hesaplayacaktık.
df.describe().T
df.loc[df["day_diff"] <= 30, "overall"].mean() * 28/100 + \
    df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 90), "overall"].mean() * 26/100 + \
    df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean() * 24/100 + \
    df.loc[(df["day_diff"]) > 180, "overall"].mean() * 22/100
# sonuç: ağırlıklı ortalama ile (4.6987161061560725)
df["overall"].mean() #(4.587589013224822)

# fonksiyonlaştırmak istersek;
def time_based_weighted_average(dataframe, w1=0.28, w2=0.26, w3=0.24, w4=0.22):
    return df.loc[df["day_diff"] <= 30, "overall"].mean() * w1+ \
                df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 90), "overall"].mean() * w2 + \
                df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean() * w3 + \
                df.loc[(df["day_diff"]) > 180, "overall"].mean() * w4

time_based_weighted_average(df) #(4.6987161061560725)

print("time_based_weighted_average", time_based_weighted_average(df))
print("overall_mean", df["overall"].mean())
print("day_diff değişkenine %28 ağırlık verdiğimizde puan",(time_based_weighted_average(df) - df["overall"].mean()), " birim artış gösteriyor. Bu demektirki ürün son dönemde bir miktar daha iyi olarak değerlendiriliyor.")

###################################################
# Görev 2: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.
###################################################

###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################
df.head()
# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.

df["helpful_no"] = df["total_vote"] - df["helpful_yes"]

###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################
def score_pos_neg_diff(up, down):
    return up - down  #Kaynak fikri çok basit: +1 oy, yorumu yukarı; –1 oy, yorumu aşağı çeker.
                      #“Bu yorumu kaç kişi fazla faydalı bulmuş?”
                      # formül = up – down

def score_average_rating(up, down):
    return 0 if up+down == 0 else up / (up + down)   #Faydalılık oranı: Bu yoruma oy verenlerin yüzde kaçı ‘Evet yardımcı’ dedi?”
                                                    #Klasik oran (p̂): helpful_yes / total_votes
                                                    # 0 – 1 arasında değer alır; 1’e ne kadar yakınsa yorum “oy birliğiyle faydalı” demektir.
                                                    # 3 👍 0 👎 → 1.00 (ama sadece 3 oy var)
                                                    #100 👍 20 👎 → 0.83 (120 oy var, muhtemelen daha güvenilir)

def wilson_lower_bound(up, down, confidence=0.95):
    n = up + down                                    #Aynı oranın %95 güvenle “en az şu kadarı yardımcı demiştir” alt sınırı
    if n == 0:                                       #Aşağıdaki Wilson formülü
        return 0                                     
    z = st.norm.ppf(1 - (1-confidence)/2)     
    phat = up / n                            
    return (phat + z*z/(2*n) -
            z*math.sqrt(phat*(1-phat)/n + z*z/(4*n*n))) / (1 + z*z/n)

#Skorları hesaplayıp veri setine ekleyelim.

df['score_pos_neg_diff']   = df.apply(lambda x: score_pos_neg_diff(
                                            x['helpful_yes'], x['helpful_no']), axis=1)   #yukarıdaki fonksiyonda yapılanları getirir.

df['score_average_rating'] = df.apply(lambda x: score_average_rating(
                                            x['helpful_yes'], x['helpful_no']), axis=1)

df['wilson_lower_bound']   = df.apply(lambda x: wilson_lower_bound(
                                            x['helpful_yes'], x['helpful_no']), axis=1)
df.head()
##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################
top20 = (df.sort_values("wilson_lower_bound", ascending=False)
           .head(20)
           .loc[:, ["reviewerID", "summary", "overall",
                    "helpful_yes", "helpful_no", "wilson_lower_bound"]])

print(top20.to_string(index=False))

#Neden Wilson Lower Bound?
#Sadece oy farkına (diff) bakmak, az oy alan yorumları gereksizce öne çıkarabilir.
#Oran (average rating) yüksek olsa bile örneklem küçükse güven düşüktür. örn:
#yüksek oran, ama küçük örneklem:
#örn → 2 kişiden 2’si “Yardımcı” dedi ⇒ Oran = 2 / 2 = 1.00 (yani %100).
#Ama sadece 2 kişi oy verdi. Yarın 3. kişi “Yardımcı değil” dese oran 2/3 = 0.67’ye düşer.
#Güvenimiz düşük, çünkü sonuç 1–2 yeni oyla kolayca değişir. örneklem yani oy veren sayısı düşük.

#WLB hem orana hem oy sayısına bakar ve %95 güvenle “en az bu kadar iyidir” diyerek güvenilir, dengeli bir sıralama üretir.

#Bu 20 yorum, sayfa üstünde “en faydalı” bölümünde gösterilmeye hazırdır.
