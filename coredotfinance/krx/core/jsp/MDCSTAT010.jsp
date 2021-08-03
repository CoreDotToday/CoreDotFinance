
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT010_FORM" method="post" name="MDCSTAT010_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[11010] 전체지수 시세</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>지수</span>
<span>파생 및 기타지수</span>
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
<input checked="" id="clssCd_0" name="clssCd" type="radio" value="0201"/><label for="clssCd_0">선물지수</label><input id="clssCd_1" name="clssCd" type="radio" value="0202"/><label for="clssCd_1">옵션지수</label><input id="clssCd_2" name="clssCd" type="radio" value="0300"/><label for="clssCd_2">전략지수</label><input id="clssCd_3" name="clssCd" type="radio" value="0600"/><label for="clssCd_3">상품지수</label>
<span class="ml30"></span>
<select id="idxMidclssCd" name="idxMidclssCd"></select>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__101418530',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="idxMidclssCd"]');

      
      var params = {
        baseName: 'krx.mdc.i18n.component',
        key: 'B148.bld'
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
      

      
      api.util.submitAjax({
        method: 'GET',
        url: '/comm/bldAttendant/executeForResourceBundle.cmd',
        data: params,
        async: false,
        success: function (data) {
          var output = data['result']['output'];
          output.forEach(function (item) {
            var option = [];
            $.each(item, function (key, value) {
              option.push(value);
            });
            var $option = $('<OPTION>').attr('value', option[0]).text(option[1]);
            if (option[0] === '') $option.prop('selected', true);
            $element.append($option);
          });
        }
      });
      

      

      
    }
  });
</script>
</td>
</tr>
<tr>
<th scope="row">조회일자</th>
<td>
<div class="cal-wrap"><input id="trdDd" name="trdDd" type="text" value="20210803"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__101418532',
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
    name: 'SEARCH_COMPONENT__101418533',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT010_')['getList']($(this));
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
<div id="jsGrid_MDCSTAT010_0">
<table>
<thead>
<tr>
<th name="IDX_NM" scope="col" width="220px">지수명</th>
<th align="right" name="CLSPRC_IDX" scope="col" width="100px">종가</th>
<th align="right" name="CMPPREVDD_IDX" scope="col" width="100px">대비</th>
<th align="right" name="FLUC_RT" scope="col" width="100px">등락률</th>
<th align="right" name="OPNPRC_IDX" scope="col" width="100px">시가</th>
<th align="right" name="HGPRC_IDX" scope="col" width="100px">고가</th>
<th align="right" name="LWPRC_IDX" scope="col" width="100px">저가</th>
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
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (경)인덱스사업부,  고객센터 (1577-0088)</span>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT010_',
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
      var $f = $content.select('#MDCSTAT010_FORM');

      self.resizeGrid = function (e) {
        self.grid.setHeight(e.getContentLeftHeight());
        self.grid.resize();
      };

      // 계열구분 콤보 이벤트 핸들러 정의
      $('#MDCSTAT010_FORM input[name="clssCd"]').click(function () {
        var $idxMidclssCd = $('select[name="idxMidclssCd"]', $f);

        // 전략지수
        if ( $(this).val() == '0300' ) {
          $idxMidclssCd.css('visibility', 'visible').prop('disabled', false);
        }
        // 그외
        else {
          $idxMidclssCd.css('visibility','hidden').prop('disabled', true);
        }
      }).filter(':eq(0)').click();

      self.init = function () {
        self.grid = api.util.grid.init({
          node: api.getModuleNode().getNode(),
          form: $f,
          layout: 'no-apply',
          grid: [
            {
              template: $content.select('#jsGrid_MDCSTAT010_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT01001',
              bldDataKey: 'output',
              fluctuation: {
                reference: 'FLUC_TP_CD',
                column: [
                  {
                    name: 'CMPPREVDD_IDX',
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
        self.grid.appendRow();
        self.grid.resize();
      }

    }
  });
</script>
