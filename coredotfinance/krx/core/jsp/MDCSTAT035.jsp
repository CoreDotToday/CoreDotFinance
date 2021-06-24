
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT035_FORM" method="post" name="MDCSTAT035_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[12021] PER/PBR/배당수익률(개별종목)</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>주식</span>
<span>세부안내</span>
<span>PER/PBR/배당수익률(개별종목)</span>
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
<th scope="row">조회구분</th>
<td>
<input checked="" id="searchType_0" name="searchType" type="radio" value="1"/><label for="searchType_0">전종목</label><input id="searchType_1" name="searchType" type="radio" value="2"/><label for="searchType_1">개별추이</label>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__160124813',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="searchType"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT035_')['chgSearchBox']($(this));
        });
      

      
    }
  });
</script>
</td>
</tr>
<tr class="jsS1">
<th scope="row">시장구분</th>
<td>
<input checked="" id="mktId_0" name="mktId" type="radio" value="ALL"/><label for="mktId_0">전체</label><input id="mktId_1" name="mktId" type="radio" value="STK"/><label for="mktId_1">KOSPI</label><input id="mktId_2" name="mktId" type="radio" value="KSQ"/><label for="mktId_2">KOSDAQ</label>
</td>
</tr>
<tr class="jsS1">
<th scope="row">조회일자</th>
<td>
<div class="cal-wrap"><input id="trdDd" name="trdDd" type="text" value="20210622"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__160124814',
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
<tr class="jsS2">
<th scope="row">종목명</th>
<td>
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
<input id="param1isuCd_finder_stkisu0" name="param1isuCd_finder_stkisu0" type="hidden" value="ALL">
<input id="" name="" type="hidden" value="">
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
                  mdc.module.getModule('MDCSTAT035_')['getList']($sel('#tboxisuCd_finder_stkisu0'));
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
</input></input></input></input></input></td>
</tr>
<tr class="jsS2">
<th scope="row">조회기간</th>
<td>
<div class="cal-wrap"><input id="startCalender" name="strtDd" placeholder="기간 시작일" type="text" value="20210615"/><input id="endCalendar" name="endDd" placeholder="기간 종료일" type="text" value="20210622"/></div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__160124816',
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
</td>
</tr>
</tbody>
</table>
<a class="btn_black btn_component_search" href="javascript:void(0);" id="jsSearchButton" name="search">조회</a>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__160124817',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT035_')['getList']($(this));
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
<div id="jsGrid_MDCSTAT035_0">
<table>
<thead>
<tr>
<th align="center" name="ISU_SRT_CD" scope="col" width="70px">종목코드</th>
<th name="ISU_ABBRV_STR" scope="col" width="135px">종목명</th>
<th align="right" name="TDD_CLSPRC" scope="col" width="65px">종가</th>
<th align="right" name="CMPPREVDD_PRC" scope="col" width="65px">대비</th>
<th align="right" name="FLUC_RT" scope="col" width="60px">등락률</th>
<th align="right" data-sorttype="stringNumber" name="EPS" scope="col" width="60px">EPS</th>
<th align="right" data-sorttype="stringNumber" name="PER" scope="col" width="65px">PER</th>
<th align="right" data-sorttype="stringNumber" name="BPS" scope="col" width="70px">BPS</th>
<th align="right" data-sorttype="stringNumber" name="PBR" scope="col" width="55px">PBR</th>
<th align="right" data-sorttype="stringNumber" name="DPS" scope="col" width="80px">주당배당금</th>
<th align="right" data-sorttype="stringNumber" name="DVD_YLD" scope="col" width="85px">배당수익률</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="ISU_SRT_CD" name="ISU_SRT_CD"></td>
<td bind="ISU_ABBRV_STR" name="ISU_ABBRV_STR"></td>
<td bind="TDD_CLSPRC" name="TDD_CLSPRC"></td>
<td bind="CMPPREVDD_PRC" name="CMPPREVDD_PRC"></td>
<td bind="FLUC_RT" name="FLUC_RT"></td>
<td bind="EPS" name="EPS"></td>
<td bind="PER" name="PER"></td>
<td bind="BPS" name="BPS"></td>
<td bind="PBR" name="PBR"></td>
<td bind="DPS" name="DPS"></td>
<td bind="DVD_YLD" name="DVD_YLD"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT035_1">
<table>
<thead>
<tr>
<th align="center" name="TRD_DD" scope="col" width="85px">일자</th>
<th align="right" name="TDD_CLSPRC" scope="col" width="65px">종가</th>
<th align="right" name="CMPPREVDD_PRC" scope="col" width="65px">대비</th>
<th align="right" name="FLUC_RT" scope="col" width="60px">등락률</th>
<th align="right" data-sorttype="stringNumber" name="EPS" scope="col" width="60px">EPS</th>
<th align="right" name="PER" scope="col" width="60px">PER</th>
<th align="right" name="BPS" scope="col" width="60px">BPS</th>
<th align="right" name="PBR" scope="col" width="60px">PBR</th>
<th align="right" name="DPS" scope="col" width="80px">주당배당금</th>
<th align="right" name="DVD_YLD" scope="col" width="80px">배당수익률</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="TRD_DD" name="TRD_DD"></td>
<td bind="TDD_CLSPRC" name="TDD_CLSPRC"></td>
<td bind="CMPPREVDD_PRC" name="CMPPREVDD_PRC"></td>
<td bind="FLUC_RT" name="FLUC_RT"></td>
<td bind="EPS" name="EPS"></td>
<td bind="PER" name="PER"></td>
<td bind="BPS" name="BPS"></td>
<td bind="PBR" name="PBR"></td>
<td bind="DPS" name="DPS"></td>
<td bind="DVD_YLD" name="DVD_YLD"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (유)주식시장부,  (코)코스닥시장부,  고객센터 (1577-0088)</span>
<p><span class="">주</span><span><em>1.</em><dfn>PER, PBR, 배당수익률 계산을 위한 기초 데이터는 한국상장회사협의회에서 제공하는 신뢰할 수 있는 자료로부터 얻어진 것이나 당사가 그 정확성이나 완정성을 보장할 수 없습니다. 그러므로 투자참고자료로만 활용하시기 바라며, 어떠한 경우에도 증권투자 결과에 대한 법적 책임소재의 증빙자료로 사용될 수 없음을 알려드립니다.</dfn></span></p>
<p><span class="">주</span><span><em>2.</em><dfn>개별종목의 EPS, BPS, 주당배당금은 최근 사업보고서 자료를 토대로 하며, 기업이벤트에 따른 조정사항이 반영됩니다.<br/><em></em><span class="depth2">EPS = (지배주주지분 당기순이익 중 보통주 귀속분)/(보통주 가중평균 유통주식수)</span><br/><em></em><span class="depth2">BPS = (지배주주지분 자본총계)/(기말 보통주+우선주 발행주식수)</span></dfn></span></p>
<p><span class="">주</span><span><em>3.</em><dfn>12월 결산법인 사업보고서 자료는 다음해 5월초부터 반영되며, 이는 사업보고서 제출기간(3개월) 및 해당자료 전반의 취합 및 검토과정(1개월)에 따른 시차입니다.</dfn></span></p>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT035_',
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
      var $f = $content.select('#MDCSTAT035_FORM');

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
              template: $content.select('#jsGrid_MDCSTAT035_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03501',
              bldDataKey: 'output',
              unit: {
                share: [],
                money: []
              },
              fluctuation: {
                reference: 'FLUC_TP_CD',
                column: [
                  {
                    name: 'CMPPREVDD_PRC',
                    useArrow: true
                  },
                  {
                    name: 'FLUC_RT'
                  }/*,
                  {
                    name: 'EPS',
                    nvl: '-'
                  }*/
                ]
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT035_1'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03502',
              bldDataKey: 'output',
              unit: {
                share: [],
                money: []
              },
              fluctuation: {
                reference: 'FLUC_TP_CD',
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

        var p_searchType = '';
        if(p_searchType) {
          $content.select('[name="searchType"]:radio[value="' + p_searchType + '"]').prop('checked', true);
          self.changeSecugrp(p_searchType);
        }
        else {
          self.changeSecugrp('1');
        }

        self.getList();

      };

      self.chgSearchBox = function () {
        var value = $f.find('[name="searchType"]:checked').val();
        self.changeSecugrp(value);
      };

      self.changeSecugrp = function(checkVal) {
        if (checkVal === '1') {
          $f.find('.jsS1').show();
          $f.find('.jsS2').hide();
        } else {
          $f.find('.jsS1').hide();
          $f.find('.jsS2').show();
        }
      };

      self.getList = function () {
        var value = $f.find('[name="searchType"]:checked').val();
        var index = 0;
        if (value === '1') index = 0;
        else if (value === '2') index = 1;
        self.grid.setIndex(index);
        self.grid.show();
        self.grid.appendRow();
        self.grid.resize();
      }
    }
  });
</script>
