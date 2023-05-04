import re
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
import pyarabic.araby
from textblob import TextBlob

stops = set(stopwords.words("arabic"))  # assign all stop words
# stop words
stop_word = {"،", "آض", "آمينَ", "آه", "آهاً", "آي", "أ", "أب", "أجل", "أجمع", "أخ", "أخذ", "أصبح", "أضحى",
             "أقبل", "أقل", "أكثر", "ألا", "أم", "أما", "أمامك", "أمامكَ", "أمسى", "أمّا", "أن", "أنا", "أنت",
             "أنتم", "أنتما", "أنتن", "أنتٝ", "أنشأ", "أنّى", "أو", "أوشك", "أولئك", "أولئكم", "أولاء",
             "أولالك", "أوّهْ", "أي", "أيا", "أين", "أينما", "أيّ", "أَنَّ", "أََيّٝ", "أّٝٝٝ", "إذ", "إذا",
             "إذاً", "إذما", "إذن", "إلى", "إليكم", "إليكما", "إليكنّ", "إليكَ", "إلَيْكَ", "إلّا", "إمّا",
             "إن", "إنّما", "إي", "إياك", "إياكم", "إياكما", "إياكن", "إيانا", "إياه", "إياها", "إياهم",
             "إياهما", "إياهن", "إياي", "إيهٝ", "إٝنَّ", "ا", "ابتدأ", "اثر", "اجل", "احد", "اخرى", "اخلولق",
             "اذا", "اربعة", "ارتدّ", "استحال", "اطار", "اعادة", "اعلنت", "اٝ", "اكثر", "اكد", "الألاء",
             "الألى", "الا", "الاخيرة", "الان", "الاول", "الاولى", "التى", "التي", "الثاني", "الثانية",
             "الذاتي", "الذى", "الذي", "الذين", "السابق", "الٝ", "اللائي", "اللاتي", "اللتان", "اللتيا",
             "اللتين", "اللذان", "اللذين", "اللواتي", "الماضي", "المقبل", "الوقت", "الى", "اليوم", "اما",
             "امام", "امس", "ان", "انبرى", "انقلب", "انه", "انها", "او", "اول", "اي", "ايار", "ايام", "ايضا",
             "ب", "بات", "باسم", "بان", "بخٝ", "برس", "بسبب", "بسّ", "بشكل", "بضع", "بطآن", "بعد", "بعض", "بك",
             "بكم", "بكما", "بكن", "بل", "بلى", "بما", "بماذا", "بمن", "بن", "بنا", "به", "بها", "بي", "بيد",
             "بين", "بَسْ", "بَلْهَ", "بٝئْسَ", "تانٝ", "تانٝك", "تبدّل", "تجاه", "تحوّل", "تلقاء", "تلك",
             "تلكم", "تلكما", "تم", "تينك", "تَيْنٝ", "تٝه", "تٝي", "ثلاثة", "ثم", "ثمّ", "ثمّة", "ثٝمَّ",
             "جعل", "جلل", "جميع", "جير", "حار", "حاشا", "حاليا", "حاي", "حتى", "حرى", "حسب", "حم", "حوالى",
             "حول", "حيث", "حيثما", "حين", "حيَّ", "حَبَّذَا", "حَتَّى", "حَذارٝ", "خلا", "خلال", "دون",
             "دونك", "ذا", "ذات", "ذاك", "ذانك", "ذانٝ", "ذلك", "ذلكم", "ذلكما", "ذلكن", "ذو", "ذوا", "ذواتا",
             "ذواتي", "ذيت", "ذينك", "ذَيْنٝ", "ذٝه", "ذٝي", "راح", "رجع", "رويدك", "ريث", "رٝبَّ", "زيارة",
             "سبحان", "سرعان", "سنة", "سنوات", "سوٝ", "سوى", "سَاءَ", "سَاءَمَا", "شبه", "شخصا", "شرع",
             "شَتَّانَ", "صار", "صباح", "صٝر", "صهٝ", "صهْ", "ضد", "ضمن", "طاق", "طالما", "طٝق", "طَق", "ظلّ",
             "عاد", "عام", "عاما", "عامة", "عدا", "عدة", "عدد", "عدم", "عسى", "عشر", "عشرة", "علق", "على",
             "عليك", "عليه", "عليها", "علًّ", "عن", "عند", "عندما", "عوض", "عين", "عَدَسْ", "عَمَّا", "غدا",
             "غير", "ـ", "ٝ", "ٝان", "ٝلان", "ٝو", "ٝى", "ٝي", "ٝيم", "ٝيما", "ٝيه", "ٝيها", "قال", "قام",
             "قبل", "قد", "قطّ", "قلما", "قوة", "كأنّما", "كأين", "كأيّ", "كأيّن", "كاد", "كان", "كانت", "كذا",
             "كذلك", "كرب", "كل", "كلا", "كلاهما", "كلتا", "كلم", "كليكما", "كليهما", "كلّما", "كلَّا", "كم",
             "كما", "كي", "كيت", "كيٝ", "كيٝما", "كَأَنَّ", "كٝخ", "لئن", "لا", "لات", "لاسيما", "لدن", "لدى",
             "لعمر", "لقاء", "لك", "لكم", "لكما", "لكن", "لكنَّما", "لكي", "لكيلا", "للامم", "لم", "لما",
             "لمّا", "لن", "لنا", "له", "لها", "لو", "لوكالة", "لولا", "لوما", "لي", "لَسْتَ", "لَسْتٝ",
             "لَسْتٝم", "لَسْتٝمَا", "لَسْتٝنَّ", "لَسْتٝ", "لَسْنَ", "لَعَلَّ", "لَكٝنَّ", "لَيْتَ", "لَيْسَ",
             "لَيْسَا", "لَيْسَتَا", "لَيْسَتْ", "لَيْسٝوا", "لَٝسْنَا", "ما", "ماانٝك", "مابرح", "مادام",
             "ماذا", "مازال", "ماٝتئ", "مايو", "متى", "مثل", "مذ", "مساء", "مع", "معاذ", "مقابل", "مكانكم",
             "مكانكما", "مكانكنّ", "مكانَك", "مليار", "مليون", "مما", "ممن", "من", "منذ", "منها", "مه", "مهما",
             "مَنْ", "مٝن", "نحن", "نحو", "نعم", "نٝس", "نٝسه", "نهاية", "نَخْ", "نٝعٝمّا", "نٝعْمَ", "ها",
             "هاؤم", "هاكَ", "هاهنا", "هبّ", "هذا", "هذه", "هكذا", "هل", "هلمَّ", "هلّا", "هم", "هما", "هن",
             "هنا", "هناك", "هنالك", "هو", "هي", "هيا", "هيت", "هيّا", "هَؤلاء", "هَاتانٝ", "هَاتَيْنٝ",
             "هَاتٝه", "هَاتٝي", "هَجْ", "هَذا", "هَذانٝ", "هَذَيْنٝ", "هَذٝه", "هَذٝي", "هَيْهَاتَ", "و",
             "و6", "وا", "واحد", "واضاٝ", "واضاٝت", "واكد", "وان", "واهاً", "واوضح", "وراءَك", "وٝي", "وقال",
             "وقالت", "وقد", "وقٝ", "وكان", "وكانت", "ولا", "ولم", "ومن", "مَن", "وهو", "وهي", "ويكأنّ",
             "وَيْ", "وٝشْكَانََ", "يكون", "يمكن", "يوم", "ّأيّان"}


def removeUrlHtml(text):
    text = re.sub("<a[\s\S]*<[\s\S]a>", " ", text)  # Remove HTML link tag
    text = re.sub("<br>", " ", text)  # Remove HTML break line tag
    text = re.sub("http\S+", "", text)  # Remove URL
    return text


def removeTashkeel(text):
    text = pyarabic.araby.strip_tashkeel(text)  # Remove Tashkeel
    text = pyarabic.araby.strip_diacritics(text)  # Strip diacritics from a text, include harakats and small letters
    return text


def removeSymbolNoise(text):
    symbols = {'~', ':', "'", '+', '[', '\\', '@', '^', '{', '%', '(', '-', '"', '*', '|', ',', '&', '<', '`', '}',
               '.', '=', ']', '!', '>', ';', '?', '$', ')', '/', '،', '؟', '×', '÷', '‘', '؛'}
    text = re.sub("_", " ", text)  # Remove underscore, add space
    text = re.sub("\W", " ", text)  # Remove hashtag, add space
    text = re.sub("\d+", "", text)  # Remove digits
    return "".join([w for w in text if w not in symbols])  # Remove symbols


def removeRepeated(text):
    text = re.sub(r'(.)\1\1+', r"\1", text)  # Remove repeated
    return text


def textNormalize(text):
    text = text.strip()  # Remove end spaces
    text = re.sub("[إأٱآا]", "ا", text)  # Normalize إأٱآا to ا
    text = re.sub("ى", "ي", text)  # Normalize ى to ي
    text = re.sub("ؤ", "ء", text)  # Normalize ؤ to ء
    text = re.sub("ئ", "ء", text)  # Normalize ئ to ء
    text = re.sub("ة", "ه", text)  # Normalize ة to ه
    return text


def removeTatweel(text):
    text = pyarabic.araby.strip_tatweel(text)  # Strip Tatweel from the text
    return text


def removeStopwords(text):
    sep = TextBlob(text)
    word = sep.words  # Separate sentences into words
    return " ".join([w for w in word if w not in stops and w not in stop_word and len(w) >= 2])  # Exclude stop words


st = ISRIStemmer()


def stemmer(text):
    sep = TextBlob(text)
    words = sep.words
    cleaned = list()
    for w in words:
        cleaned.append(st.stem(w))
    return " ".join(cleaned)


def clean_youtube(text):
    text = removeSymbolNoise(text)
    text = removeRepeated(text)
    return text


# do all preprocessing functions
def doPreprocessing(text):
    text = removeUrlHtml(text)
    text = removeTashkeel(text)
    text = removeSymbolNoise(text)
    text = removeRepeated(text)
    text = textNormalize(text)
    text = removeTatweel(text)
    text = removeStopwords(text)
    text = stemmer(text)
    return text


def doPreprocessingWordCloud(text):
    text = removeUrlHtml(text)
    text = removeTashkeel(text)
    text = removeSymbolNoise(text)
    text = removeRepeated(text)
    text = removeTatweel(text)
    text = removeStopwords(text)
    return text
