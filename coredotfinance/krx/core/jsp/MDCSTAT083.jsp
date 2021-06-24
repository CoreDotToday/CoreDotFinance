
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT083_FORM" method="post" name="MDCSTAT083_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[13301] 전종목 시세</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>증권상품</span>
<span>ELW</span>
<span>전종목 시세</span>
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
<th scope="row">조회일자</th><!-- 조회일자 -->
<td>
<div class="cal-wrap"><input id="trdDd" name="trdDd" placeholder="기간" type="text" value="20210623"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__092837527',
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
    name: 'SEARCH_COMPONENT__092837531',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT083_')['getList']($(this));
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
<select class="CI-MDI-UNIT-SHARE" disabled="" name="share" style="display: none;"><option selected="" value="1">증권</option><option value="2">천증권</option><option value="3">백만증권</option></select>
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
<div id="jsGrid_MDCSTAT083_0">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="ISU_SRT_CD" rowspan="2" scope="col" width="85px">종목코드</th>
<th name="ISU_ABBRV" rowspan="2" scope="col" width="200px">종목명</th>
<th align="right" name="TDD_CLSPRC" rowspan="2" scope="col" width="80px">종가</th>
<th align="right" name="CMPPREVDD_PRC" rowspan="2" scope="col" width="70px">대비</th>
<th align="right" name="TDD_OPNPRC" rowspan="2" scope="col" width="70px">시가</th>
<th align="right" name="TDD_HGPRC" rowspan="2" scope="col" width="70px">고가</th>
<th align="right" name="TDD_LWPRC" rowspan="2" scope="col" width="70px">저가</th>
<th align="right" name="ACC_TRDVOL" rowspan="2" scope="col" width="110px">거래량</th>
<th align="right" name="ACC_TRDVAL" rowspan="2" scope="col" width="120px">거래대금</th>
<th align="right" name="MKTCAP" rowspan="2" scope="col" width="130px">시가총액</th>
<th align="right" name="LIST_SHRS" rowspan="2" scope="col" width="120px">상장증권수</th>
<th colspan="4" name="ULY" scope="col" width="420px">기초자산</th>
</tr>
<tr>
<th name="ULY_NM" parent="ULY" scope="col" width="180px">자산명</th>
<th align="right" name="ULY_PRC" parent="ULY" scope="col" width="90px">종가</th>
<th align="right" name="CMPPREVDD_PRC1" parent="ULY" scope="col" width="80px">대비</th>
<th align="right" name="FLUC_RT1" parent="ULY" scope="col" width="70px">등락률</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="ISU_SRT_CD" name="ISU_SRT_CD"></td>
<td bind="ISU_ABBRV" name="ISU_ABBRV"></td>
<td bind="TDD_CLSPRC" name="TDD_CLSPRC"></td>
<td bind="CMPPREVDD_PRC" name="CMPPREVDD_PRC"></td>
<td bind="TDD_OPNPRC" name="TDD_OPNPRC"></td>
<td bind="TDD_HGPRC" name="TDD_HGPRC"></td>
<td bind="TDD_LWPRC" name="TDD_LWPRC"></td>
<td bind="ACC_TRDVOL" name="ACC_TRDVOL"></td>
<td bind="ACC_TRDVAL" name="ACC_TRDVAL"></td>
<td bind="MKTCAP" name="MKTCAP"></td>
<td bind="LIST_SHRS" name="LIST_SHRS"></td>
<td bind="ULY_NM" name="ULY_NM"></td>
<td bind="ULY_PRC" name="ULY_PRC"></td>
<td bind="CMPPREVDD_PRC1" name="CMPPREVDD_PRC1"></td>
<td bind="FLUC_RT1" name="FLUC_RT1"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (유)증권상품시장부,  고객센터 (1577-0088)</span>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT083_',
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
      var $f = $content.select('#MDCSTAT083_FORM');

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
              template: $content.select('#jsGrid_MDCSTAT083_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT08301',
              bldDataKey: 'output',
              unit: {
                share: ['ACC_TRDVOL', 'LIST_SHRS'],
                money: ['ACC_TRDVAL', 'MKTCAP']
              },
              fluctuation: {
                reference: 'FLUC_TP_CD',
                column: [
                  {
                    name: 'CMPPREVDD_PRC',
                    useArrow: true
                  },
                  {
                    reference: 'FLUC_TP_CD1',
                    name: 'CMPPREVDD_PRC1',
                    useArrow: true
                  },
                  {
                    reference: 'FLUC_TP_CD1',
                    name: 'FLUC_RT1'
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
