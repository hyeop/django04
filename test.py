import googletrans
from googletrans import Translator
 
d = googletrans.LANGUAGES
text1 = "Հան Սյունգ-կվանը հիմար է՞"

translator = Translator()

print(translator.translate(text1, src="hy", dest="ko").text)

# for i in d:
#     trans1 = translator.translate(text1, src='ko', dest=i)
#     print(f"{d[i]} 인사 : ", trans1.text)
