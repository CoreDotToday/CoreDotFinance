
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT023_FORM" method="post" name="MDCSTAT023_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[12009] 투자자별 거래실적(개별종목)</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>주식</span>
<span>거래실적</span>
<span>투자자별 거래실적(개별종목)</span>
</p>
</h2>
<div class="search_tb">
<div data-component="search">
<table>
<colgroup>
<col class="fix_w_s5"/>
<col style="width:50%;"/>
<col/>
</colgroup>
<tbody>
<tr>
<th scope="row">조회구분</th>
<td colspan="2">
<input checked="" id="inqTpCd_0" name="inqTpCd" type="radio" value="1"/><label for="inqTpCd_0">기간합계</label><input id="inqTpCd_1" name="inqTpCd" type="radio" value="2"/><label for="inqTpCd_1">일별추이</label>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__100910098',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="inqTpCd"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT023_')['inqTpCdChg']($(this));
        });
      

      
    }
  });
</script>
<select id="trdVolVal" name="trdVolVal"><option value="1">거래량</option><option selected="" value="2">거래대금</option></select>
<select id="askBid" name="askBid"><option value="1">매도</option><option value="2">매수</option><option selected="" value="3">순매수</option></select>
</td>
</tr>
<tr>
<th scope="row">종목명</th>
<td colspan="2">
<div class="searchBoxWrap">
<div class="search">
<p>
<input autocomplete="off" id="tboxisuCd_finder_stkisu0" name="tboxisuCd_finder_stkisu0" style="width: 350px;" title="주식 종목 검색" type="text" value="005930/삼성전자"/>
<img alt="검색팝업" id="btnisuCd_finder_stkisu0" name="btnisuCd_finder_stkisu0" src="/pub/img/btn_dbg.png"/>
</p>
</div>
</div>
<input id="isuCd_finder_stkisu0" name="isuCd" type="hidden" value="KR7005930003">
<input id="isuCd_finder_stkisu02" name="isuCd2" type="hidden" value="KR7005930003">
<input id="codeNmisuCd_finder_stkisu0" name="codeNmisuCd_finder_stkisu0" type="hidden" value="삼성전자">
<input id="param1isuCd_finder_stkisu0" name="param1isuCd_finder_stkisu0" type="hidden" value="ALL"/>
<input id="" name="" type="hidden" value=""/>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'FINDER_COMPONENT_isuCd_finder_stkisu0',
    init: 'init',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $sel = $content.select;

      self.init = function () {
        
        var cookie = mdc.util.getFinderCookie(self.getCookieFinderCd());
        if(cookie.finderCd === self.getCookieFinderCd()){
          // typeNo별 쿠키종목을 구분해야하는 경우(ex 증권상품)를 위해 분기
          var typeNo = cookie.typeNo; //쿠키저장시 finder의 typeNo
          if(!typeNo){
            typeNo = '0';
          }
          if(typeNo == ('0')){
            if(cookie.codeVal)$sel('#isuCd_finder_stkisu0').val(cookie.codeVal);
            if(cookie.tbox)$sel('#tboxisuCd_finder_stkisu0').val(cookie.tbox);
            if(cookie.codeNm)$sel('#codeNmisuCd_finder_stkisu0').val(cookie.codeNm);
            if(cookie.codeVal2)$sel('#isuCd_finder_stkisu02').val(cookie.codeVal2);

            
          }
        }

        
      };

      

      $sel('#btnisuCd_finder_stkisu0').on('click', function () {

        if($sel('#tboxisuCd_finder_stkisu0').val()==""){
          self.openFinder(false);
        }else{
          self.openFinder(true);
        }

      });

      $sel('#tboxisuCd_finder_stkisu0').on('keydown', function (e) {
        if (13 == e.keyCode) {
          if($sel('#tboxisuCd_finder_stkisu0').val()==""){
            self.openFinder(false);
          }else{
            self.openFinder(true);
          }

        }
      });

      //쿠키 중복 방지
      self.getCookieFinderCd = function(){
        var cookieFinderCd = '';
        var curFinderCd = 'finder_stkisu';
        if(curFinderCd === 'finder_secuprodisu'){
          cookieFinderCd = 'finder_stkisu0';
        }
        else {
          cookieFinderCd = 'finder_stkisu';
        }
        return cookieFinderCd;
      };

      self.openFinder = function (isKeyDown) {
        var s_tboxNmVal = '';

        //캐쉬가 false/true선택관계없이 사용자가 검색어 입력시 그 값을 종목검색 팝업창에 전달
          var cookieFinderCd = self.getCookieFinderCd();
          var cookieFinderCdVal = api.util.getCookie(cookieFinderCd+'_finderCd');

            //검색텍스트박스값이 쿠키의 값과 같을경우 검색어 안넘어가도록
            var s_defaultVal = '005930/삼성전자';
            var s_tbox = api.util.getCookie(self.getCookieFinderCd()+'_tbox');

            if(s_tbox !== $sel('#tboxisuCd_finder_stkisu0').val() && s_defaultVal !== $sel('#tboxisuCd_finder_stkisu0').val()){
              s_tboxNmVal = $sel('#tboxisuCd_finder_stkisu0').val();
            }

        var params = {
          finderNo: '_finder_stkisu0',
          finderCd: 'finder_stkisu',
          typeNo: '0',
          compValue: '',
          param1 : $sel('#param1isuCd_finder_stkisu0').val(),
          tboxId : 'tboxisuCd_finder_stkisu0',
          tboxNm : s_tboxNmVal,
          codeValId : 'isuCd_finder_stkisu0',
          codeNmId : 'codeNmisuCd_finder_stkisu0',
          pnlid : '',
          disableCompValue: '',
          initSearch: 'false'
        };

        if(!isKeyDown){
          params.tboxNm = '';
        }

        if(mdc.validate.checkSearchText(params.tboxNm)){
          //= (20201120, 김정삼) 자동검색 목록을 선택목록 엔터키 입력 시 검색기 팝업 하지 않는다.
          //  >>> 개발담당자 로직 확인하자
          var $searchAuto = $sel('.search-auto');
          var visble = $searchAuto.is(':visible');
          // 목록에 1개 있을 때 enter 키인시 선택
          if ( visble && $searchAuto.find('li').length == 1 ) {
            $searchAuto.find('li').addClass('on');
          }
          var $selLi = $searchAuto.find('li.on');

          if ( visble && $selLi.length ) {
            $('a', $selLi).click();

            
                if ( $sel('#tboxisuCd_finder_stkisu0').val() != '' ) {
                  mdc.module.getModule('MDCSTAT023_')['search']($sel('#tboxisuCd_finder_stkisu0'));
                }
            

            return false;
          }
          //=/

          mdc.layer.openModal({
            appendTo: $content.getNode(),
            className: 'pop_opened pop_opened1',
            id: 'jsLayer_finder_stkisu0',
            title: '주식 종목 검색',
            width: 548,
            height: 'auto',
            url: '/comm/finder/finder_stkisu.jsp',
            useCloseButton: false,
            ajaxOption: {data: params},
            focus: $(this),
            afterAppend: function () {
              api.module.getModule('FINDER_LAYER__finder_stkisu0').procInit();
            }
          });
        }
      };

      
      
      var isEmptyCodeVal = false;
      $sel('#tboxisuCd_finder_stkisu0').on('keyup', function (e) {
        if ( e.keyCode != 13 && !isEmptyCodeVal) {
          $sel('#isuCd_finder_stkisu0').val("");
          $sel('#isuCd_finder_stkisu02').val("");
          isEmptyCodeVal = true;
        }
      });
      
    }
  });



  
  $.fn.defaultAutocomplete = $.fn.autocomplete;

  $.fn.autocomplete = function (options) {

    var _this = this;
    var isMouseUnder = false;

    var config = {
      'contextName' : 'output',
      'viewCount' : 7,
      'bldPath' : '',
      'submit' : undefined,
      'listFn' : undefined,
      'className' : 'search-auto',
      'submitClear' :  true,
      'searchCookie' : false,
      'searchCookieType' : '',
      'enterSubmit' : false,
      'param' : { }
    };

    if (options != null && options !== undefined) {
      $.extend(config, options);
    }

    var $searchAuto = $('<div></div>', {
      'class' : config.className,
      'css' : {
        'display' : 'none'
      }
    });

    $(_this).after($searchAuto);

    var submit = function (obj) {
      if (config.submit) {
        config.submit(obj);
      }
      $searchAuto.html('');
      $searchAuto.hide();
      if (config.submitClear) {
        $(_this).val('');
      }
    };

    $(_this).focusout(function () {
      if (!isMouseUnder) {
        $searchAuto.hide();
      }
    });

    $(_this).keyup(function (e) {
      if ((47 < e.keyCode && e.keyCode < 106) || (185 < e.keyCode && e.keyCode < 223) || (105 < e.keyCode && e.keyCode < 112) || 8 == e.keyCode || 46 == e.keyCode){
        if (!config.searchCookie){
          getSearchList();
        }
      }

      if (13 == e.keyCode && config.enterSubmit) {
        submit($searchAuto.find('li[data-selected=true]'));
      }

    });

    $(_this).keydown(function (e) {
      if(e.keyCode == 40) {
        var selected = $searchAuto.find('li[data-selected=true]');
        if (selected.length == 1) {
          selected.removeAttr('data-selected');
          selected.removeClass('on');

          var next = selected.next();
          next.attr('data-selected', 'true');
          next.addClass('on');
          $(_this).val(next.children('a').text());
        } else {
          var first = $searchAuto.find('li:first');
          first.attr('data-selected', 'true');
          first.addClass('on');
          $(_this).val(first.children('a').text());
        }
      }else if(e.keyCode == 38){
        var selected = $searchAuto.find('li[data-selected=true]');
        if (selected.length == 1) {
          selected.removeAttr('data-selected');
          selected.removeClass('on');

          var prev = selected.prev();
          prev.attr('data-selected', 'true');
          prev.addClass('on');
          $(_this).val(prev.children('a').text());
        } else {
          var last = $searchAuto.find('li:last');
          last.attr('data-selected', 'true');
          last.addClass('on');
          $(_this).val(last.children('a').text());
        }
      }
    }).click(function(e){
      if (config.searchCookie){
        if(Cookies.get(config.searchCookieType) != undefined){
          var schSaveData = Cookies.getJSON(config.searchCookieType);
          $ul = $('<ul/>');
          $.each(schSaveData, function(i, item){
            $ul.append('<li data-cd=\"'+ item.keyCd +'\" data-fcd=\"'+ item.KeyFullCd +'\" data-nm=\"'+ item.codNm +'\"><a href=\"#\">'+item.title+'</a></li>');
          });
          $searchAuto.html($ul);
          attachListEvent();
          $searchAuto.show();
        }
      }
    });

    var attachListEvent = function () {
      var li = $searchAuto.find('li');
      li.find('a').click(function () {
        submit($(this).parent());
        return false;
      });

      li.find('a').focusout(function () {
        $searchAuto.hide();
      });

      li.find('a').focus(function () {
        $searchAuto.show();
      });

      $searchAuto.find('ul').mouseleave(function () {
        isMouseUnder = false;
      });

      li.mouseenter(function () {
        li.removeAttr('data-selected');
        li.removeClass('on');
        var t = $(this);
        t.addClass('on');
        t.attr('data-selected', 'true');
        $(_this).val(t.children('a').text());
        isMouseUnder = true;
      });
    };

    var getSearchList = function () {
      var data = {
        'contextName' : config.contextName,
        'value' : encodeURIComponent($(_this).val()),
        'viewCount' : config.viewCount,
        'bldPath' : config.bldPath
      };
      $.extend(data, config.param);
      $.ajax({
        'url' : '/comm/finder/autocomplete.jspx',
        'data' : data,
        'success' : function (html) {
          if (html == '') {
            $searchAuto.hide();
          } else {
            var ul = '<ul>'+html+'</ul>';
            $searchAuto.html(ul);
            if (config.listFn) {
              config.listFn($searchAuto);
            }
            attachListEvent();
            $searchAuto.show();
          }
        }
      });
    };
  };

  $('#tboxisuCd_finder_stkisu0').autocomplete({
    'contextName' : 'finder_stkisu',
    'bldPath' : '/dbms/comm/finder/finder_stkisu_autocomplete',
    'viewCount' : 5,
    'submit' : function (li) {

      var shotCd = li.attr('data-tp');
      var fullCd = li.attr('data-cd');
      var codeNm = li.attr('data-nm');
      var mktNm = 'ALL';

      $('#codeNmisuCd_finder_stkisu0').val(li.attr('data-nm'));
      $('#isuCd_finder_stkisu0').val(li.attr('data-cd'));
      $('#isuCd_finder_stkisu02').val(li.attr('data-tp'));

      // 지수면 명칭만
      if ( 'ISU' === 'IDX' ) {
        $('#tboxisuCd_finder_stkisu0').val(li.attr('data-nm'));
      }
      // 회사면 발행기관 코드
      else if ( 'ISU' === 'COM' ) {
        $('#tboxisuCd_finder_stkisu0').val(li.attr('data-cd')+'/'+li.attr('data-nm'));
      }
      // 그외 코드/명칭
      else {
        $('#tboxisuCd_finder_stkisu0').val(li.attr('data-tp')+'/'+li.attr('data-nm'));
      }

      var input = {
        finderCd: 'finder_stkisu',
        tbox: shotCd +'/'+ codeNm,
        codeNm: codeNm,
        codeVal: fullCd,
        codeVal2: fullCd,
        typeNo: '',
        param1: mktNm
      };

      //= (20201202, 김정삼)
      if ( 'ISU' === 'IDX' ) {//지수
        input.tbox = codeNm;
        input.codeVal2 = shotCd;
      }
      //=/
      mdc.util.setFinderCookie(input);

      return false;
    },
    'submitClear' : false
  });
  
</script>
</input></input></input></td>
</tr>
<tr>
<th scope="row">조회기간</th>
<td>
<div class="cal-wrap"><input id="strtDd" name="strtDd" type="text" value="20210616"/><input id="endDd" name="endDd" type="text" value="20210623"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__100910099',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="endDd"]');

      
      var params = {
        baseName: 'krx.mdc.i18n.component',
        key: 'B122.bld'
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
            var compId = 'B122';
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
            var datePeriod = '-7d';
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
<!--component:search type="date" dateType="calendar" name="strtDd|endDd" id="strtDd|endDd" datePeriod="-7d" compId="B122" compIdDateLimit="B128" isDateLimit="true" /-->
</td>
<td>
<div>
<input id="detailView_0" name="detailView" type="checkbox" value="1"/><label for="detailView_0">상세보기</label>
</div>
</td>
</tr>
</tbody>
</table>
<a class="btn_black btn_component_search" href="javascript:void(0);" id="jsSearchButton" name="search">조회</a>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__100910100',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT023_')['search']($(this));
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
<div id="jsGrid_MDCSTAT023_0">
<table>
<thead>
<tr>
<th align="center" name="INVST_TP_NM" rowspan="2" scope="col" sortable="false" width="100px">투자자구분</th>
<th colspan="3" name="TRDVOL" scope="col" width="350px">거래량</th>
<th colspan="3" name="TRDVAL" scope="col" width="430px">거래대금</th>
</tr>
<tr>
<th align="right" name="ASK_TRDVOL" parent="TRDVOL" scope="col" sortable="false" width="120px">매도</th>
<th align="right" name="BID_TRDVOL" parent="TRDVOL" scope="col" sortable="false" width="120px">매수</th>
<th align="right" name="NETBID_TRDVOL" parent="TRDVOL" scope="col" sortable="false" width="110px">순매수</th>
<th align="right" name="ASK_TRDVAL" parent="TRDVAL" scope="col" sortable="false" width="150px">매도</th>
<th align="right" name="BID_TRDVAL" parent="TRDVAL" scope="col" sortable="false" width="150px">매수</th>
<th align="right" name="NETBID_TRDVAL" parent="TRDVAL" scope="col" sortable="false" width="130px">순매수</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="INVST_TP_NM" name="INVST_TP_NM"></td>
<td bind="ASK_TRDVOL" name="ASK_TRDVOL"></td>
<td bind="BID_TRDVOL" name="BID_TRDVOL"></td>
<td bind="NETBID_TRDVOL" name="NETBID_TRDVOL"></td>
<td bind="ASK_TRDVAL" name="ASK_TRDVAL"></td>
<td bind="BID_TRDVAL" name="BID_TRDVAL"></td>
<td bind="NETBID_TRDVAL" name="NETBID_TRDVAL"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT023_1">
<table>
<thead>
<tr>
<th align="center" name="TRD_DD" scope="col" width="100px">일자</th>
<th align="right" name="TRDVAL1" scope="col" width="150px">기관 합계</th>
<th align="right" name="TRDVAL2" scope="col" width="150px">기타법인</th>
<th align="right" name="TRDVAL3" scope="col" width="150px">개인</th>
<th align="right" name="TRDVAL4" scope="col" width="150px">외국인 합계</th>
<th align="right" name="TRDVAL_TOT" scope="col" width="160px">전체</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="TRD_DD" name="TRD_DD"></td>
<td bind="TRDVAL1" name="TRDVAL1"></td>
<td bind="TRDVAL2" name="TRDVAL2"></td>
<td bind="TRDVAL3" name="TRDVAL3"></td>
<td bind="TRDVAL4" name="TRDVAL4"></td>
<td bind="TRDVAL_TOT" name="TRDVAL_TOT"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT023_2">
<table>
<thead>
<tr>
<th align="center" name="TRD_DD" scope="col" width="100px">일자</th>
<th align="right" name="TRDVAL1" scope="col" width="150px">기관 합계</th>
<th align="right" name="TRDVAL2" scope="col" width="150px">기타법인</th>
<th align="right" name="TRDVAL3" scope="col" width="150px">개인</th>
<th align="right" name="TRDVAL4" scope="col" width="150px">외국인 합계</th>
<th align="right" name="TRDVAL_TOT" scope="col" width="160px">전체</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="TRD_DD" name="TRD_DD"></td>
<td bind="TRDVAL1" name="TRDVAL1"></td>
<td bind="TRDVAL2" name="TRDVAL2"></td>
<td bind="TRDVAL3" name="TRDVAL3"></td>
<td bind="TRDVAL4" name="TRDVAL4"></td>
<td bind="TRDVAL_TOT" name="TRDVAL_TOT"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT023_3">
<table>
<thead>
<tr>
<th align="center" name="TRD_DD" scope="col" width="100px">일자</th>
<th align="right" name="TRDVAL1" scope="col" width="100px">금융투자</th>
<th align="right" name="TRDVAL2" scope="col" width="100px">보험</th>
<th align="right" name="TRDVAL3" scope="col" width="100px">투신</th>
<th align="right" name="TRDVAL4" scope="col" width="100px">사모</th>
<th align="right" name="TRDVAL5" scope="col" width="100px">은행</th>
<th align="right" name="TRDVAL6" scope="col" width="100px">기타금융</th>
<th align="right" name="TRDVAL7" scope="col" width="100px">연기금 등</th>
<th align="right" name="TRDVAL8" scope="col" width="100px">기타법인</th>
<th align="right" name="TRDVAL9" scope="col" width="100px">개인</th>
<th align="right" name="TRDVAL10" scope="col" width="100px">외국인</th>
<th align="right" name="TRDVAL11" scope="col" width="100px">기타외국인</th>
<th align="right" name="TRDVAL_TOT" scope="col" width="110px">전체</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="TRD_DD" name="TRD_DD"></td>
<td bind="TRDVAL1" name="TRDVAL1"></td>
<td bind="TRDVAL2" name="TRDVAL2"></td>
<td bind="TRDVAL3" name="TRDVAL3"></td>
<td bind="TRDVAL4" name="TRDVAL4"></td>
<td bind="TRDVAL5" name="TRDVAL5"></td>
<td bind="TRDVAL6" name="TRDVAL6"></td>
<td bind="TRDVAL7" name="TRDVAL7"></td>
<td bind="TRDVAL8" name="TRDVAL8"></td>
<td bind="TRDVAL9" name="TRDVAL9"></td>
<td bind="TRDVAL10" name="TRDVAL10"></td>
<td bind="TRDVAL11" name="TRDVAL11"></td>
<td bind="TRDVAL_TOT" name="TRDVAL_TOT"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT023_4">
<table>
<thead>
<tr>
<th align="center" name="TRD_DD" scope="col" width="100px">일자</th>
<th align="right" name="TRDVAL1" scope="col" width="130px">금융투자</th>
<th align="right" name="TRDVAL2" scope="col" width="120px">보험</th>
<th align="right" name="TRDVAL3" scope="col" width="130px">투신</th>
<th align="right" name="TRDVAL4" scope="col" width="130px">사모</th>
<th align="right" name="TRDVAL5" scope="col" width="120px">은행</th>
<th align="right" name="TRDVAL6" scope="col" width="130px">기타금융</th>
<th align="right" name="TRDVAL7" scope="col" width="130px">연기금 등</th>
<th align="right" name="TRDVAL8" scope="col" width="130px">기타법인</th>
<th align="right" name="TRDVAL9" scope="col" width="140px">개인</th>
<th align="right" name="TRDVAL10" scope="col" width="130px">외국인</th>
<th align="right" name="TRDVAL11" scope="col" width="120px">기타외국인</th>
<th align="right" name="TRDVAL_TOT" scope="col" width="140px">전체</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="TRD_DD" name="TRD_DD"></td>
<td bind="TRDVAL1" name="TRDVAL1"></td>
<td bind="TRDVAL2" name="TRDVAL2"></td>
<td bind="TRDVAL3" name="TRDVAL3"></td>
<td bind="TRDVAL4" name="TRDVAL4"></td>
<td bind="TRDVAL5" name="TRDVAL5"></td>
<td bind="TRDVAL6" name="TRDVAL6"></td>
<td bind="TRDVAL7" name="TRDVAL7"></td>
<td bind="TRDVAL8" name="TRDVAL8"></td>
<td bind="TRDVAL9" name="TRDVAL9"></td>
<td bind="TRDVAL10" name="TRDVAL10"></td>
<td bind="TRDVAL11" name="TRDVAL11"></td>
<td bind="TRDVAL_TOT" name="TRDVAL_TOT"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (유)주식시장부,  (코)코스닥시장부,  (넥)코넥스시장부,  고객센터 (1577-0088)</span>
<p><span class="">주</span><span><dfn>당일 매매내역은 당일 정규시장 마감 이후(오후 3시45분 예정) 반영되며, 시간외 등의 매매내역이 포함된 최종 매매내역은 당일자 마감 이후(오후 6시 예정) 제공됩니다.</dfn></span></p>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT023_',
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
      var $f = $content.select('#MDCSTAT023_FORM');

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
              template: $content.select('#jsGrid_MDCSTAT023_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT02301',
              bldDataKey: 'output',
              lateInfoYn: false,
              unit: {
                share: ['ASK_TRDVOL', 'BID_TRDVOL', 'NETBID_TRDVOL'],
                money: ['ASK_TRDVAL', 'BID_TRDVAL', 'NETBID_TRDVAL']
              },
              applyRowBg: false,
              customRowBg: {
                reference: 'CONV_OBJ_TP_CD',
                row: [
                  {
                    key: 'GB',
                    color: '#E4E4E4'
                  },
                  {
                    key: 'SS',
                    color: '#F8F8F8'
                  },
                  {
                    key: 'TS',
                    color: '#F0F0F0'
                  }
                ]
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT023_1'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT02302',
              bldDataKey: 'output',
              unit: {
                share: ['TRDVAL1', 'TRDVAL2', 'TRDVAL3', 'TRDVAL4', 'TRDVAL_TOT'],
                money: []
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT023_2'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT02302',
              bldDataKey: 'output',
              unit: {
                share: [],
                money: ['TRDVAL1', 'TRDVAL2', 'TRDVAL3', 'TRDVAL4', 'TRDVAL_TOT']
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT023_3'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT02303',
              bldDataKey: 'output',
              unit: {
                share: ['TRDVAL1', 'TRDVAL2', 'TRDVAL3', 'TRDVAL4', 'TRDVAL5', 'TRDVAL6', 'TRDVAL7', 'TRDVAL8', 'TRDVAL9', 'TRDVAL10', 'TRDVAL11', 'TRDVAL_TOT'],
                money: []
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT023_4'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT02303',
              bldDataKey: 'output',
              unit: {
                share: [],
                money: ['TRDVAL1', 'TRDVAL2', 'TRDVAL3', 'TRDVAL4', 'TRDVAL5', 'TRDVAL6', 'TRDVAL7', 'TRDVAL8', 'TRDVAL9', 'TRDVAL10', 'TRDVAL11', 'TRDVAL_TOT']
              }
            }            
          ]
        });

        self.inqTpCdChg();
        self.search();
      };

      self.search = function () {
        var value = $f.find('[name="inqTpCd"]:checked').val();
        var detailChk = $f.find('[name="detailView"]').is(":checked");
        var trdVolVal = $f.find('[name="trdVolVal"]').val();

        if ($f.find('[name="isuCd"]').val() === '') {
          mdc.layer.alert(mdc.lang.getMessage('MG002'));
          return;
        }

        var index = 0;
        if (value === '1') index = 0;
        else if (value === '2' && trdVolVal === '1' && detailChk === false) index = 1;
        else if (value === '2' && trdVolVal === '2' && detailChk === false) index = 2;
        else if (value === '2' && trdVolVal === '1' && detailChk === true) index = 3;
        else if (value === '2' && trdVolVal === '2' && detailChk === true) index = 4;
        
        self.grid.setIndex(index); // 한 화면에 조건에 따라 다수의 그리드가 존재할 때 보여줄 그리드 인덱스 설정
        self.grid.show(); // 위에 설정한 인덱스의 그리드를 보여주고 다른 그리드는 모두 숨김
        self.grid.appendRow(); // 설정한 form 과 bld 를 바탕으로 서비스 조회 후 그리드에 데이터 삽입
        self.grid.resize(); // MDI 화면 특성 상 append 후 리사이즈 필수
      }
      
      self.inqTpCdChg = function () {
        var inqTpCd = $f.find('[name="inqTpCd"]:checked').val();
        if(inqTpCd=="1"){
          $f.find('[name="trdVolVal"]').hide();
          $f.find('[name="askBid"]').hide();
          $f.find('[name="detailView"]').closest('div').hide();
        }
        else {
          $f.find('[name="trdVolVal"]').show();
          $f.find('[name="askBid"]').show();
          $f.find('[name="detailView"]').closest('div').show();
        }

      }
      
      
    }
  });
</script>
