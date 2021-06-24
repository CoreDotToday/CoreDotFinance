
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT016_FORM" method="post" name="MDCSTAT016_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[12002] 전종목 등락률</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>주식</span>
<span>종목시세</span>
<span>전종목 등락률</span>
</p>
</h2>
<div class="search_tb">
<div data-component="search">
<table>
<colgroup>
<col class="fix_w_s5"/>
<col/>
</colgroup>
<tbody>
<tr>
<th scope="row">시장구분</th>
<td>
<input checked="" id="mktId_0" name="mktId" type="radio" value="ALL"/><label for="mktId_0">전체</label><input id="mktId_1" name="mktId" type="radio" value="STK"/><label for="mktId_1">KOSPI</label><input id="mktId_2" name="mktId" type="radio" value="KSQ"/><label for="mktId_2">KOSDAQ</label><input id="mktId_3" name="mktId" type="radio" value="KNX"/><label for="mktId_3">KONEX</label>
</td>
</tr>
<tr>
<th scope="row">조회기간</th>
<td>
<div class="cal-wrap"><input id="strdDd" name="strtDd" type="text" value="20210613"><input id="endDd" name="endDd" type="text" value="20210621"/></input></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__150536718',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="endDd"]');

      
      var params = {
        baseName: 'krx.mdc.i18n.component',
        key: 'B128.bld'
      };

      var queryString = 'null';
      if (queryString && queryString !== 'null') {
        var queryArray = queryString.split('&');
        queryArray.forEach(function (query) {
          var name = query.split('=')[0];
          var value = query.split('=')[1] || '';
          params[name] = value;
        });
      }
      

      
        
          var calendarOption = {};
          var input = [];
          
            
              
              input.push($content.select('[name="strtDd"]'));
              
              input.push($content.select('[name="endDd"]'));
              
            
          

          
          var date = '';
          api.util.submitAjax({
            method: 'GET',
            url: '/comm/bldAttendant/executeForResourceBundle.cmd',
            async: false,
            data: params,
            success: function (data) {
              var output = data['result']['output'];
              output.forEach(function (item) {
                $.each(item, function (key, value) {
                  date = value;
                });
              });
            }
          });

          if (date) {
            input.forEach(function (item) {
              item.val(date);
            });

            //=== (20201028, 김정삼) compIdDateLimit 값을 지정한 경우 이 지정값(bld)으로 달력팝업활성화 종료일 기준을 변경한다
            
            calendarOption.limit = date;

            var compIdDateLimit = 'B128';
            var compId = 'B128';
            if (compIdDateLimit && compIdDateLimit !== compId) {
              api.util.submitAjax({
                method: 'GET',
                url: '/comm/bldAttendant/executeForResourceBundle.cmd',
                async: false,
                data: $.extend(params, {key: compIdDateLimit + '.bld'}),
                success: function (data) {
                  var output = data['result']['output'];
                  output.forEach(function (item) {
                    $.each(item, function (key, value) {
                      calendarOption.limit = value;
                    });
                  });
                }
              });
            }
            
            //===/

            //=== (20201215, 김상훈) restictId 값을 지정한 경우 이 지정값(bld)으로 조회가능 시작일을 제한한다.
            
            var restictId = 'B155';
            var menuId = mdc.getMdiView() ? mdc.getMdiView().id : '';

            if (restictId && (menuId !== '' && menuId !== undefined)) {
              params['menuId'] = menuId;
              api.util.submitAjax({
                method: 'GET',
                url: '/comm/bldAttendant/executeForResourceBundle.cmd',
                async: false,
                data: $.extend(params, {key: restictId + '.bld'}),
                success: function (data) {
                  var output = data['result']['output'];
                  calendarOption.restrictDate = output[0]['restrict_date'];
                }
              });
            }
            
            //===/

            
            // 기간 재계산
            var datePeriod = '-8d';
            var periodType = datePeriod.substring(datePeriod.length - 1); // +-d, +-m, +-y
            var period = Number(datePeriod.substring(0, datePeriod.length - 1));
            date = api.util.calcDate(date).getCalcDate(periodType, Math.abs(period));

            //20201215 김상훈, 달력 시작일자가 제한일보다 전일인 경우 제한일을 시작일로 설정
            if(calendarOption.restrictDate != undefined && date < calendarOption.restrictDate){
              date = calendarOption.restrictDate;
            }

            if (period >= 0) input[input.length - 1].val(date);
            else input[0].val(date);
            

          }
          

          calendarOption.input = input;
          calendarOption.positionTop = false;
          calendarOption.showButton = true;
          calendarOption.disabledDate = 'null';
          calendarOption.disabledTp = 'null';
          calendarOption.changeStrtDate = 'false';
          $.fn.calendar(calendarOption);
        

        
      

      

      
    }
  });
</script>
<input checked="" id="adjStkPrc_check_0" name="adjStkPrc_check" type="checkbox" value="Y"/><label for="adjStkPrc_check_0">수정주가 적용</label>
<input name="adjStkPrc" type="hidden" value="2">
</input></td>
</tr>
</tbody>
</table>
<a class="btn_black btn_component_search" href="javascript:void(0);" id="jsSearchButton" name="search">조회</a>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__150536721',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT016_')['getList']($(this));
        });
      

      
    }
  });
</script>
</div>
<button class="CI-MDI-COMPONENT-BUTTON btn_close_tggle" type="button">Close</button>
</div>
<div class="CI-MDI-UNIT-WRAP">
<div class="time CI-MDI-UNIT" data-view-sequence="0">
<p class="CI-MDI-UNIT-TIME"></p>
<p>
<select class="CI-MDI-UNIT-SHARE" disabled="" name="share" style="display: none;"><option selected="" value="1">주</option><option value="2">천주</option><option value="3">백만주</option></select>
<select class="CI-MDI-UNIT-MONEY" disabled="" name="money" style="display: none;"><option selected="" value="1">원</option><option value="2">천원</option><option value="3">백만원</option><option value="4">십억원</option></select>
<button class="CI-MDI-UNIT-FILTER" type="button"><img src="/templets/mdc/img/btn_time2.png" title="컬럼필터 팝업"/></button>
<button class="CI-MDI-UNIT-DOWNLOAD" type="button"><img src="/templets/mdc/img/btn_time1.png" title="다운로드 팝업"/></button>
</p>
</div>
</div>
<script type="text/javascript">
(function(mdc, $) {
  var $sel = $('select[name="otherUnit"].CI-MDI-UNIT-MONEY');
  if ( $('option',$sel).length <= 1 ) { $sel.addClass('bg_none'); }
}(window.mdc, jQuery));
</script>
</form>
<div id="jsGrid_MDCSTAT016_0">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="ISU_SRT_CD" scope="col" width="80px">종목코드</th>
<th name="ISU_ABBRV" scope="col" width="150px">종목명</th>
<th align="right" name="BAS_PRC" scope="col" width="95px">시작일 기준가</th>
<th align="right" name="TDD_CLSPRC" scope="col" width="95px">종료일 종가</th>
<th align="right" name="CMPPREVDD_PRC" scope="col" width="80px">대비</th>
<th align="right" name="FLUC_RT" scope="col" width="80px">등락률</th>
<th align="right" name="ACC_TRDVOL" scope="col" width="100px">거래량</th>
<th align="right" name="ACC_TRDVAL" scope="col" width="140px">거래대금</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="ISU_SRT_CD" name="ISU_SRT_CD"></td>
<td bind="ISU_ABBRV" name="ISU_ABBRV"></td>
<td bind="BAS_PRC" name="BAS_PRC"></td>
<td bind="TDD_CLSPRC" name="TDD_CLSPRC"></td>
<td bind="CMPPREVDD_PRC" name="CMPPREVDD_PRC"></td>
<td bind="FLUC_RT" name="FLUC_RT"></td>
<td bind="ACC_TRDVOL" name="ACC_TRDVOL"></td>
<td bind="ACC_TRDVAL" name="ACC_TRDVAL"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (유)주식시장부,  (코)코스닥시장부,  (넥)코넥스시장부,  고객센터 (1577-0088)</span>
<p><span class="">주</span><span><em>1.</em><dfn>조회기간 종료일을 당일자로 지정하는 경우, 종료일종가에는 당일 장중 가격이 표시됩니다.</dfn><em>2.</em><dfn>거래량/거래대금은 조회기간 동안의 누적 규모에 해당합니다.</dfn><em>3.</em><dfn>수정주가란 유무상증자, 주식배당, 액면변경 등으로 주가가 연속성을 잃고 단층현상이 생기게 되는 경우, 주가 비교의 연속성을 위해 기준시점(권리락일 등)을 기준으로 이전 시점의 주가를 조정한 가격입니다. 이용자께서는 필요에 따라 수정주가 사용여부를 선택하시어 주가등락률 정보를 활용하시기 바랍니다.</dfn></span></p>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT016_',
    init: 'init',
    mdi: {
      name: mdc.module.getMdiModuleName(),
      event: {
        afterViewActivated: ['resizeGrid'],
        afterViewSizeChanged: ['resizeGrid']
      }
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $f = $content.select('#MDCSTAT016_FORM');
      var f = $f[0];

      self.resizeGrid = function (e) {
        self.grid.setHeight(e.getContentLeftHeight());
        self.grid.resize();
      };

      self.init = function () {
        self.grid = api.util.grid.init({
          node: api.getModuleNode().getNode(),
          form: $f,
          layout: 'no-apply',
          grid: [
            {
              template: $content.select('#jsGrid_MDCSTAT016_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT01602',
              bldDataKey: 'OutBlock_1',
              unit: {
                share: ['ACC_TRDVOL'],
                money: ['ACC_TRDVAL']
              },
              fluctuation: {
                reference: 'FLUC_TP',
                column: [
                  {
                    name: 'CMPPREVDD_PRC',
                    useArrow: true
                  },
                  {
                    name: 'FLUC_RT'
                  }
                ]
              }
            }
          ]
        });

        self.getList();
      };

      self.getList = function () {
        f.adjStkPrc.value = $content.select('[name="adjStkPrc_check"]').prop('checked') ? 2 : 1;
        self.grid.appendRow(); // 설정한 form 과 bld 를 바탕으로 서비스 조회 후 그리드에 데이터 삽입
      };
    }
  });
</script>
