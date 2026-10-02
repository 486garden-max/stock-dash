import hashlib
import html
import json
from datetime import date

import pandas as pd
import streamlit as st

from ui_v2 import hero, card
from automatic import brief
from bi_view import theme, overview, detail, peers_chart
from chat_research import published, parse_bundle, trends, growth, request_text


def render_research(store, state, sample_mode):
    theme()
    hero('내 자산', '관심종목부터 시장 흐름과 최근 공시까지 한 화면에서 확인하세요.', 'STOCKDASH · HOME')
    if sample_mode:
        st.info('둘러보기 중입니다. 개인 목록을 저장하려면 먼저 대시보드 비밀번호를 설정하세요.')
    else:
        with st.expander('＋ 종목 추가', expanded=not state.get('stocks')):
            with st.form('research_manual'):
                name = st.text_input('종목명', placeholder='예: 삼성전자')
                with st.expander('종목코드를 알고 있다면 · 선택'):
                    code = st.text_input('종목코드', max_chars=6)
                if st.form_submit_button('내 목록에 추가'):
                    import re
                    if not name.strip() or (code and not re.fullmatch(r'[0-9]{6}', code)):
                        st.error('종목명과 숫자 6자리 코드를 확인하세요. 코드는 생략할 수 있습니다.')
                    else:
                        known = next((s for s in state.get('stocks', []) if s['name'].strip().casefold() == name.strip().casefold()), {})
                        identity = known.get('code') or code or 'pending-' + hashlib.sha256(name.strip().casefold().encode()).hexdigest()[:16]
                        try:
                            store.save_stock({'code':identity, 'name':name.strip(), 'kind':known.get('kind','관심')})
                            st.rerun()
                        except Exception: st.error('목록 저장에 실패했습니다. 저장 공간 설정을 확인하세요.')
    # Premium home dashboard: asset → chart → watchlist → market → holdings → disclosures
    snapshot = st.session_state.get('account_snapshot') or {}
    account_value = snapshot.get('value')
    account_pnl = snapshot.get('pnl')
    cash = snapshot.get('cash')
    positions = snapshot.get('positions') or []
    saved = state.get('stocks', [])

    st.markdown('<div class="planx-dashboard-section"><span class="planx-dashboard-section-title">내 자산</span><span class="planx-dashboard-section-sub">계좌 연결 시 실시간 반영</span></div>', unsafe_allow_html=True)
    value_text = f"{account_value:,.0f}원" if account_value is not None else "계좌 연결 필요"
    pnl_text = f"{account_pnl:+,.0f}원" if account_pnl is not None else "손익 정보 없음"
    pnl_class = "color:#ef4444" if account_pnl is not None and account_pnl < 0 else "color:#16a34a"
    cash_text = f"{cash:,.0f}원" if cash is not None else "—"
    st.markdown(f'''
<div class="planx-home-asset">
  <div><div class="planx-home-asset-label">총 평가자산</div>
  <div class="planx-home-asset-value">{html.escape(value_text)}</div>
  <div class="planx-home-asset-change" style="{pnl_class}">평가손익 {html.escape(pnl_text)}</div></div>
  <div class="planx-home-asset-side">예수금&nbsp;&nbsp; <strong style="color:#333b46">{html.escape(cash_text)}</strong><br>국내주식 평가액 기준</div>
</div>''', unsafe_allow_html=True)

    st.markdown('<div class="planx-home-chart"><div class="planx-home-chart-title">자산 추이</div>', unsafe_allow_html=True)
    asset_history = snapshot.get('history') or snapshot.get('asset_history') or []
    if asset_history:
        try:
            chart_df = pd.DataFrame(asset_history)
            date_col = next((k for k in ['date','day','at'] if k in chart_df.columns), None)
            value_col = next((k for k in ['value','asset_value','total_value'] if k in chart_df.columns), None)
            if date_col and value_col:
                chart_df[date_col] = pd.to_datetime(chart_df[date_col], errors='coerce')
                chart_df[value_col] = pd.to_numeric(chart_df[value_col], errors='coerce')
                chart_df = chart_df.dropna(subset=[date_col, value_col]).sort_values(date_col).set_index(date_col)
                if not chart_df.empty:
                    st.line_chart(chart_df[value_col], height=190, use_container_width=True)
                else:
                    st.caption('계좌 연결 후 자산 추이 데이터가 표시됩니다.')
            else:
                st.caption('계좌 연결 후 자산 추이 데이터가 표시됩니다.')
        except Exception:
            st.caption('계좌 연결 후 자산 추이 데이터가 표시됩니다.')
    else:
        st.caption('계좌 연결 후 일자별 자산 데이터가 쌓이면 이곳에 추이가 표시됩니다.')
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="planx-dashboard-section"><span class="planx-dashboard-section-title">관심종목</span><span class="planx-dashboard-section-sub">옆으로 넘겨 빠르게 확인</span></div>', unsafe_allow_html=True)
    watch = [s for s in saved if s.get('code') != 'SAMPLE']
    if watch:
        cards = []
        for item in watch:
            name = html.escape(item.get('name','종목'))
            code = html.escape(item.get('code','종목코드 대기'))
            report = item.get('report') or {}
            price = report.get('price')
            price_text = f"{price:,.0f}원" if price else "분석 필요"
            cards.append(f'<div class="planx-watch-scroll-card"><div class="planx-watch-name">{name}</div><div class="planx-watch-price">{html.escape(price_text)}</div><div class="planx-watch-meta">{code}</div></div>')
        st.markdown('<div class="planx-horizontal-scroll">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="planx-empty"><strong style="color:#333b46">관심종목을 추가해보세요</strong><br><span>자주 보는 종목을 추가하면 이곳에서 빠르게 확인할 수 있습니다.</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="planx-dashboard-section"><span class="planx-dashboard-section-title">시장지수</span><span class="planx-dashboard-section-sub">주요 시장 흐름</span></div>', unsafe_allow_html=True)
    market_html = []
    for title in ["KOSPI", "KOSDAQ", "원/달러", "거래대금"]:
        market_html.append(f'<div class="planx-market-card"><div class="planx-market-name">{title}</div><div class="planx-market-value">데이터 연결 필요</div><div class="planx-market-change">시장 API 연결 후 표시</div></div>')
    st.markdown('<div class="planx-market-row">' + ''.join(market_html) + '</div>', unsafe_allow_html=True)

    st.markdown('<div class="planx-dashboard-section"><span class="planx-dashboard-section-title">보유종목</span><span class="planx-dashboard-section-sub">내 계좌 현황</span></div>', unsafe_allow_html=True)
    if positions:
        rows_html = ['<div class="planx-holdings"><div class="planx-holdings-head"><div>종목</div><div style="text-align:right">평가금액</div><div style="text-align:right">평가손익</div><div style="text-align:right">수익률</div><div style="text-align:right">비중</div></div>']
        for p in positions:
            name = html.escape(str(p.get('name','종목')))
            code = html.escape(str(p.get('code','')))
            value = p.get('value')
            pnl = p.get('pnl')
            ret = p.get('return') if p.get('return') is not None else p.get('profit_rate')
            weight = p.get('weight')
            value_text = f"{value:,.0f}원" if value is not None else "—"
            pnl_text = f"{pnl:+,.0f}원" if pnl is not None else "—"
            ret_text = f"{ret:+.1f}%" if isinstance(ret,(int,float)) else "—"
            weight_text = f"{weight:.1f}%" if isinstance(weight,(int,float)) else "—"
            rows_html.append(f'<div class="planx-holdings-row"><div class="planx-holdings-name">{name}<span class="planx-holdings-code">{code}</span></div><div class="planx-holdings-num">{value_text}</div><div class="planx-holdings-num">{pnl_text}</div><div class="planx-holdings-num">{ret_text}</div><div class="planx-holdings-num">{weight_text}</div></div>')
        rows_html.append('</div>')
        st.markdown(''.join(rows_html), unsafe_allow_html=True)
    else:
        st.markdown('<div class="planx-empty"><strong style="color:#333b46">보유종목이 없습니다</strong><br><span>계좌를 연결하면 실제 보유종목이 표 형태로 표시됩니다.</span></div>', unsafe_allow_html=True)

    st.markdown('<div class="planx-dashboard-section"><span class="planx-dashboard-section-title">최근 공시</span><span class="planx-dashboard-section-sub">최근 확인된 기업 공시</span></div>', unsafe_allow_html=True)
    notices = []
    for item in saved:
        for n in (item.get('report') or {}).get('disclosures', []):
            notices.append({**n, 'stock_name': item.get('name','')})
    notices.sort(key=lambda x: x.get('date',''), reverse=True)
    if notices:
        disclosure_rows = ['<div class="planx-holdings">']
        for n in notices[:6]:
            url = html.escape(n.get('url','#'), quote=True)
            date_text = html.escape(str(n.get('date','')))
            stock_name = html.escape(str(n.get('stock_name','')))
            title = html.escape(str(n.get('title','')))
            disclosure_rows.append(f'<div class="planx-disclosure"><div class="planx-disclosure-date">{date_text}</div><div class="planx-disclosure-stock">{stock_name}</div><div class="planx-disclosure-title"><a href="{url}" target="_blank">{title}</a></div></div>')
        disclosure_rows.append('</div>')
        st.markdown(''.join(disclosure_rows), unsafe_allow_html=True)
    else:
        st.markdown('<div class="planx-empty"><strong style="color:#333b46">최근 공시가 없습니다</strong><br><span>종목을 분석하면 최신 수집 공시가 이곳에 표시됩니다.</span></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 종목 분석")
    research = published()
    for r in state.get('chat_research', []):
        if r['code'] not in research or r['as_of'] >= research[r['code']]['as_of']: research[r['code']] = r
    stocks = {s['code']:s for s in state.get('stocks', [])}
    for p in st.session_state.get('account_snapshot', {}).get('positions', []):
        stocks[p['code']] = {**stocks.get(p['code'], {}), 'code':p['code'], 'name':p['name']}
    with st.expander('조사 요청 · 최신 내용으로 업데이트'):
        st.write('① 종목을 추가하거나 포트폴리오에서 계좌를 불러옵니다. ② 아래 요청문을 복사해 지금 대화창에 보냅니다. ③ 조사 결과가 반영되면 이 화면을 새로고침합니다.')
        st.code(request_text(list(stocks.values())), language=None)
        st.caption('요청문에는 종목명만 포함됩니다. 이 채팅에 요청문을 보내야 조사가 시작됩니다.')
        if st.button('반영된 조사 결과 다시 읽기'): st.rerun()
        if not sample_mode:
            with st.expander('조사 파일 가져오기 · 고급'):
                upload = st.file_uploader('별도로 받은 조사 JSON 가져오기 · 선택', type=['json'])
                if upload and st.button('조사 파일 검증·저장'):
                    try:
                        reports = parse_bundle(upload.getvalue())
                        def save(data):
                            merged = {r['code']:r for r in data.get('chat_research', [])}
                            for r in reports:
                                if r['code'] not in merged or r['as_of'] >= merged[r['code']]['as_of']: merged[r['code']] = r
                            data['chat_research'] = list(merged.values())
                        store.change(save)
                        st.rerun()
                    except (ValueError, KeyError, TypeError): st.error('조사 파일의 형식·출처·기간을 확인하세요. 기존 결과는 유지했습니다.')
                    except Exception: st.error('저장에 실패했습니다. 기존 결과는 유지했습니다.')
    if not stocks:
        with st.container(border=True):
            st.subheader('첫 관심종목을 담아보세요')
            st.write('위의 종목 추가를 열고 기업 이름 하나만 입력하면 시작할 수 있습니다.')
            st.caption('계좌가 있다면 왼쪽 계좌 연결에서 보유종목을 가져올 수도 있습니다.')
        return
    rows, details = [], {}
    for key, stock in stocks.items():
        r = research.get(key)
        if not r and key.startswith('pending-'):
            matches = [v for v in research.values() if v['name'].strip().casefold() == stock['name'].strip().casefold()]
            if len(matches) == 1: r = matches[0]
        r = r or {}
        f, v, flow = r.get('financial') or {}, r.get('valuation') or {}, r.get('flow') or {}
        trend, frame = trends(r.get('prices'), r.get('as_of', date.today().isoformat()))
        row = {'종목':stock['name'], '코드':r.get('code', key if not key.startswith('pending-') else '확인 필요'),
               '누적 매출 성장':growth(f['revenue'], f['prior_revenue']) if f else '조사 필요',
               '누적 영업이익 성장':growth(f['operating_profit'], f['prior_operating_profit']) if f else '조사 필요',
               '외국인 / 기관':f"{flow['foreign']:+,.0f} / {flow['institution']:+,.0f} {flow['unit']}" if flow else '조사 필요',
               '적정주가 참고':f"{v['base']:,.0f}원" if v else '조사 필요',
               '일봉':trend['daily'], '주봉':trend['weekly'], '조사일':r.get('as_of','미조사')}
        rows.append(row);details[key]=(stock, r, trend, frame)
    overview(details, st.session_state.get('account_snapshot'))
    with st.expander('전체 지표 비교'):
        st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)
    st.markdown('### 기업 하나를 깊게 보기')
    selected = st.selectbox('자세히 볼 종목', list(details), format_func=lambda k:stocks[k]['name'], key='research_selected')
    stock, r, trend, frame = details[selected]
    if not r:
        st.info('이 종목의 채팅 조사 결과가 아직 없습니다. 위 요청문을 대화창에 보내면 조사 결과를 채울 수 있습니다.')
        if stock.get('report'):
            st.write('기존 공식 결산 분석: ' + brief(stock['report'])['summary'])
        return
    st.subheader(stock['name'])
    st.caption('조사일 ' + r['as_of'] + ' · 각 표의 자료 기간은 아래에 별도 표시합니다. 실시간 분석이 아닙니다.')
    detail(r)
    summary = r.get('summary')
    if summary:
        with st.container(border=True):
            st.markdown('**핵심 요약**')
            st.write(summary['text'])
    tabs = st.tabs(['어떤 기업인가요?', '실적은 어떤가요?', '주가 흐름', '가격과 확인 사항'])
    with tabs[0]:
        for label, key in [('주력사업과 기업 특징','business')]:
            st.subheader(label)
            entry = r.get(key)
            if entry:
                st.write(entry['text']); st.link_button('설명의 원문 근거', entry['source'], key='research_'+key)
            else: st.info('조사 필요')
    with tabs[1]:
        f = r.get('financial')
        if f:
            st.caption(f"누적 {f['period']} / 전년 {f['prior_period']} · {f['basis']} · {f['currency']} {f['unit']}")
            st.dataframe([{'항목':'매출','이번 누적':f['revenue'],'전년 누적':f['prior_revenue'],'변화':growth(f['revenue'],f['prior_revenue'])},
                          {'항목':'영업이익','이번 누적':f['operating_profit'],'전년 누적':f['prior_operating_profit'],'변화':growth(f['operating_profit'],f['prior_operating_profit'])}], hide_index=True)
            st.link_button('실적 근거', f['source'])
        else: st.info('전년 같은 기간 누적 실적 조사 필요')
        peers = r.get('peers')
        st.subheader('경쟁사 영업이익 순위')
        if peers and peers['rows']:
            st.write(peers['selection_reason'])
            st.caption(f"비교 표본 내 순위 · {peers['period']} · {peers['basis']} · {peers['currency']} {peers['unit']}")
            peers_chart(peers)
            df = pd.DataFrame(peers['rows']);df['순위'] = df['operating_profit'].rank(method='min', ascending=False).astype(int)
            st.dataframe(df.sort_values('순위')[['순위','name','operating_profit','source']].rename(columns={'name':'기업','operating_profit':'영업이익','source':'출처'}), hide_index=True)
        else: st.info('같은 기간·회계기준의 경쟁사 실적 조사 필요')
    with tabs[2]:
        flow = r.get('flow')
        if flow:
            st.caption(flow['start'] + ' ~ ' + flow['end'] + ' · 순매수 ' + flow['unit'])
            a,b=st.columns(2);a.metric('외국인 순매수', f"{flow['foreign']:+,.0f}");b.metric('기관 순매수', f"{flow['institution']:+,.0f}")
            st.link_button('수급 근거', flow['source'])
        else: st.info('외국인·기관 수급 조사 필요')
        a,b=st.columns(2);a.metric('일봉 추세',trend['daily']);b.metric('완료 주봉 추세',trend['weekly'])
        st.caption('수정종가 기준: 일봉 20·60일, 주봉 10·20주 평균과 장기 평균 기울기를 함께 확인합니다. 진행 중인 주는 제외합니다.')
        if frame is not None:
            st.caption('가격 자료 마지막 거래일 ' + str(frame['date'].iloc[-1]))
            st.line_chart(frame.set_index('date')['close'])
            st.link_button('가격 자료 근거', r['prices']['source'])
    with tabs[3]:
        v = r.get('valuation')
        if v:
            a,b,c=st.columns(3)
            for col,key,label in [(a,'low','낮은 참고가'),(b,'base','기본 참고가'),(c,'high','높은 참고가')]: col.metric(label,f"{v[key]:,.0f}원")
            st.write(v['method']);st.caption(f"비교 가격 {v['current_price']:,.0f}원 · {v['price_date']} · 기본 참고가 대비 차이 {(v['base']/v['current_price']-1)*100:+.1f}%")
            st.link_button('평가 근거', v['source'])
        else: st.info('평가 가정과 가격 근거 조사 필요')
        for gap in r.get('data_gaps', []): st.write('확인 필요 · ' + str(gap))
    if not sample_mode:
        with st.expander('투자일지 남기기'):
            with st.form('research_note'):
                note=st.text_area('투자일지 · 다음 확인할 조건')
                if st.form_submit_button('기록 저장') and note.strip():
                    try:
                        from datetime import datetime, timezone
                        store.log('journal', {'code':selected,'at':datetime.now(timezone.utc).isoformat(),'kind':'note','note':note.strip()})
                        st.success('일지를 저장했습니다.')
                    except Exception: st.error('저장 실패. 입력 내용을 보관하세요.')
