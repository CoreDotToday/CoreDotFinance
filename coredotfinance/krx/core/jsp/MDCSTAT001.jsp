
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT001_FORM" method="post" name="MDCSTAT001_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[11001] 전체지수 시세</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>지수</span>
<span>주가지수</span>
<span>전체지수 시세</span>
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
<th scope="row">계열구분</th>
<td>
<input checked="" id="idxIndMidclssCd_0" name="idxIndMidclssCd" type="radio" value="01"/><label for="idxIndMidclssCd_0">KRX</label><input id="idxIndMidclssCd_1" name="idxIndMidclssCd" type="radio" value="02"/><label for="idxIndMidclssCd_1">KOSPI</label><input id="idxIndMidclssCd_2" name="idxIndMidclssCd" type="radio" value="03"/><label for="idxIndMidclssCd_2">KOSDAQ</label><input id="idxIndMidclssCd_3" name="idxIndMidclssCd" type="radio" value="04"/><label for="idxIndMidclssCd_3">테마</label>
</td>
</tr>
<tr>
<th scope="row">조회일자</th>
<td>
<div class="cal-wrap"><input id="trdDd" name="trdDd" type="text" value="20210803"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__094241093',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="trdDd"]');

      
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
          
            
              
              input.push($content.select('[name="trdDd"]'));
              
            
          

          
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
</td>
</tr>
</tbody>
</table>
<a class="btn_black btn_component_search" href="javascript:void(0);" id="jsSearchButton" name="search">조회</a>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__094241094',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT001_')['getList']($(this));
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
<select class="CI-MDI-UNIT-SHARE" disabled="" name="share" style="display: none;"><option value="1">주</option><option selected="" value="2">천주</option><option value="3">백만주</option></select>
<select class="CI-MDI-UNIT-MONEY" disabled="" name="money" style="display: none;"><option value="1">원</option><option value="2">천원</option><option selected="" value="3">백만원</option><option value="4">십억원</option></select>
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
<div id="jsGrid_MDCSTAT001_0">
<table>
<thead>
<tr>
<th name="IDX_NM" scope="col" width="170px">지수명</th>
<th align="right" name="CLSPRC_IDX" scope="col" width="80px">종가</th>
<th align="right" name="CMPPREVDD_IDX" scope="col" width="85px">대비</th>
<th align="right" name="FLUC_RT" scope="col" width="70px">등락률</th>
<th align="right" name="OPNPRC_IDX" scope="col" width="80px">시가</th>
<th align="right" name="HGPRC_IDX" scope="col" width="80px">고가</th>
<th align="right" name="LWPRC_IDX" scope="col" width="80px">저가</th>
<th align="right" name="ACC_TRDVOL" scope="col" width="100px">거래량</th>
<th align="right" name="ACC_TRDVAL" scope="col" width="130px">거래대금</th>
<th align="right" name="MKTCAP" scope="col" width="150px">상장시가총액</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="IDX_NM" name="IDX_NM"></td>
<td bind="CLSPRC_IDX" name="CLSPRC_IDX"></td>
<td bind="CMPPREVDD_IDX" name="CMPPREVDD_IDX"></td>
<td bind="FLUC_RT" name="FLUC_RT"></td>
<td bind="OPNPRC_IDX" name="OPNPRC_IDX"></td>
<td bind="HGPRC_IDX" name="HGPRC_IDX"></td>
<td bind="LWPRC_IDX" name="LWPRC_IDX"></td>
<td bind="ACC_TRDVOL" name="ACC_TRDVOL"></td>
<td bind="ACC_TRDVAL" name="ACC_TRDVAL"></td>
<td bind="MKTCAP" name="MKTCAP"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (경)인덱스사업부,  고객센터 (1577-0088)</span>
<p><span class="">주</span><span><dfn>코스피지수와 코스닥지수의 경우, 지수 산출시에는 외국주를 포함하지 않으며, 지수 산출관련통계(거래량, 거래대금, 시가총액 등)의 산출시에만 외국주 포함여부를 구분하여 자료를 제공합니다.</dfn></span></p>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT001_',
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
      var $f = $content.select('#MDCSTAT001_FORM');

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
              template: $content.select('#jsGrid_MDCSTAT001_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT00101',
              bldDataKey: 'output',
              unit: {
                share: ['ACC_TRDVOL'],
                money: ['ACC_TRDVAL', 'MKTCAP']
              },
              fluctuation: {
                reference: 'FLUC_TP_CD',
                column: [
                  {
                    name: 'CMPPREVDD_IDX',
                    useArrow: true,
                    nvl: '-'
                  },
                  {
                    name: 'FLUC_RT',
                    nvl: '-'
                  }
                ]
              }
            }
          ]
        });

        self.getList();
      };

      self.getList = function () {
        self.grid.appendRow();
        self.grid.resize();
      }
    }
  });
</script>
