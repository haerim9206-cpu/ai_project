# 1. 스트림릿 클라우드 한글 깨짐 방지를 위한 폰트 다운로드 설정
@st.cache_data
def load_korean_font():
    font_url = "https://github.com/google/fonts/raw/main/ofl/nanumgothic/NanumGothic-Regular.ttf"
    font_path = "NanumGothic.ttf"
    
    # 폰트 파일이 로컬(서버)에 없으면 다운로드
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    
    # [수정된 부분] Matplotlib 버전에 상관없이 안전하게 폰트를 등록하는 방식
    try:
        # 최신 Matplotlib 버전용 객체 생성 방식
        fm.FontManager().addfont(font_path)
    except AttributeError:
        # 이전 Matplotlib 버전용 방식
        fm.font_manager.addfont(font_path)
        
    font_prop = fm.FontProperties(fname=font_path)
    plt.rc('font', family=font_prop.get_name())
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
