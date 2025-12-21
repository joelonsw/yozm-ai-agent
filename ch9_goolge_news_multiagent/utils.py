import re
from datetime import datetime, timedelta

def clean_html(html_text: str) -> str:
    """HTML 태그를 제거하고 텍스트만 반환"""
    if not html_text:
        return ""

    clean_text = re.sub(r"<.*?>", "", html_text)
    clean_text = re.sub(r"\s+", " ", clean_text).strip()
    return clean_text

def truncate_text(text: str, max_length: int = 500) -> str:
    if not text or len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def format_date(date_string: str) -> str:
    """날짜 포맷정리"""
    if not date_string:
        return "날짜 정보 없음"

    try:
        if "GMT" in date_string:
            date_string = date_string.split("GMT")[0].strip()
        return date_string
    except Exception:
        return date_string

def convert_gmt_to_kst(gmt_time_str: str) -> str:
    """GMT 시간을 KST로 변환"""
    KST_OFFSET_HOURS = 9
    gmt_time = datetime.strptime(gmt_time_str, "%a, %d %b %Y %H:%M:%S GMT")
    kst_time = gmt_time + timedelta(hours=KST_OFFSET_HOURS)
    return kst_time.strftime("%Y-%m-%d %H:%M:%S")