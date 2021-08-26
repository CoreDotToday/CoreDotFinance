
<style>
  input[type=checkbox] + label {line-height: 0}
  input[type=checkbox] {top: 0}
</style>
<form action="null" class="CI-MDI-COMPONENT-WRAP" id="MDCSTAT034_FORM" method="post" name="MDCSTAT034_FORM" onsubmit="return false;">
<h2 class="tit_h2">
<p>[12020] 상장회사 상세검색</p>
<p class="address_top">
<span><img alt="홈으로 이동" src="/templets/mdc/img/ico_house.png"/></span>
<span>통계</span>
<span>기본 통계</span>
<span>주식</span>
<span>세부안내</span>
<span>상장회사 상세검색</span>
</p>
</h2>
<div class="search_tb">
<div data-component="search">
<table>
<colgroup>
<col class="fix_w_s5"/>
<col/>
<col class="fix_w_s5"/>
<col/>
</colgroup>
<tbody>
<tr>
<th scope="row">시장구분</th>
<td colspan="3">
<input checked="" id="mktTpCd_0" name="mktTpCd" type="radio" value="0"/><label for="mktTpCd_0">전체</label><input id="mktTpCd_1" name="mktTpCd" type="radio" value="1"/><label for="mktTpCd_1">KOSPI</label><input id="mktTpCd_2" name="mktTpCd" type="radio" value="2"/><label for="mktTpCd_2">KOSDAQ</label><input id="mktTpCd_3" name="mktTpCd" type="radio" value="6"/><label for="mktTpCd_3">KONEX</label>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__141525727',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="mktTpCd"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT034_')['chgMktId']($(this));
        });
      

      
    }
  });
</script>
</td>
</tr>
<tr>
<th scope="row">종목명</th>
<td colspan="3">
<div class="searchBoxWrap">
<div class="search">
<p>
<input autocomplete="off" id="tboxisuSrtCd_finder_listisu0" name="tboxisuSrtCd_finder_listisu0" style="width: 350px;" title="상장 종목 검색" type="text" value="전체"/>
<img alt="검색팝업" id="btnisuSrtCd_finder_listisu0" name="btnisuSrtCd_finder_listisu0" src="/pub/img/btn_dbg.png"/>
</p>
</div>
<a align="left" class="btn_black2 smaller" href="#" id="btnClearisuSrtCd_finder_listisu0" name="btnClearisuSrtCd_finder_listisu0">초기화</a>
</div>
<input id="isuSrtCd_finder_listisu0" name="isuSrtCd" type="hidden" value="ALL">
<input id="isuSrtCd_finder_listisu02" name="isuSrtCd2" type="hidden" value="ALL">
<input id="codeNmisuSrtCd_finder_listisu0" name="codeNmisuSrtCd_finder_listisu0" type="hidden" value="">
<input id="param1isuSrtCd_finder_listisu0" name="param1isuSrtCd_finder_listisu0" type="hidden" value="">
<input id="" name="" type="hidden" value="">
<script type="text/javascript">
  mdc.module.setModule({
    name: 'FINDER_COMPONENT_isuSrtCd_finder_listisu0',
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
            if(cookie.codeVal)$sel('#isuSrtCd_finder_listisu0').val(cookie.codeVal);
            if(cookie.tbox)$sel('#tboxisuSrtCd_finder_listisu0').val(cookie.tbox);
            if(cookie.codeNm)$sel('#codeNmisuSrtCd_finder_listisu0').val(cookie.codeNm);
            if(cookie.codeVal2)$sel('#isuSrtCd_finder_listisu02').val(cookie.codeVal2);

            
          }
        }

        
      };

      
      $sel('#btnClearisuSrtCd_finder_listisu0').on('click', function () {
        $sel('#tboxisuSrtCd_finder_listisu0').val("전체");
        $sel('#isuSrtCd_finder_listisu0').val("ALL");
        $sel('#isuSrtCd_finder_listisu02').val("ALL");
      });
      

      $sel('#btnisuSrtCd_finder_listisu0').on('click', function () {

        if($sel('#tboxisuSrtCd_finder_listisu0').val()==""){
          self.openFinder(false);
        }else{
          self.openFinder(true);
        }

      });

      $sel('#tboxisuSrtCd_finder_listisu0').on('keydown', function (e) {
        if (13 == e.keyCode) {
          if($sel('#tboxisuSrtCd_finder_listisu0').val()==""){
            self.openFinder(false);
          }else{
            self.openFinder(true);
          }

        }
      });

      //쿠키 중복 방지
      self.getCookieFinderCd = function(){
        var cookieFinderCd = '';
        var curFinderCd = 'finder_listisu';
        if(curFinderCd === 'finder_secuprodisu'){
          cookieFinderCd = 'finder_listisu0';
        }
        else {
          cookieFinderCd = 'finder_listisu';
        }
        return cookieFinderCd;
      };

      self.openFinder = function (isKeyDown) {
        var s_tboxNmVal = '';

        //캐쉬가 false/true선택관계없이 사용자가 검색어 입력시 그 값을 종목검색 팝업창에 전달
          var cookieFinderCd = self.getCookieFinderCd();
          var cookieFinderCdVal = api.util.getCookie(cookieFinderCd+'_finderCd');

            //검색텍스트박스값이 쿠키의 값과 같을경우 검색어 안넘어가도록
            var s_defaultVal = '전체';
            var s_tbox = api.util.getCookie(self.getCookieFinderCd()+'_tbox');

            if(s_tbox !== $sel('#tboxisuSrtCd_finder_listisu0').val() && s_defaultVal !== $sel('#tboxisuSrtCd_finder_listisu0').val()){
              s_tboxNmVal = $sel('#tboxisuSrtCd_finder_listisu0').val();
            }

        var params = {
          finderNo: '_finder_listisu0',
          finderCd: 'finder_listisu',
          typeNo: '0',
          compValue: '',
          param1 : $sel('#param1isuSrtCd_finder_listisu0').val(),
          tboxId : 'tboxisuSrtCd_finder_listisu0',
          tboxNm : s_tboxNmVal,
          codeValId : 'isuSrtCd_finder_listisu0',
          codeNmId : 'codeNmisuSrtCd_finder_listisu0',
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

            
                if ( $sel('#tboxisuSrtCd_finder_listisu0').val() != '' ) {
                  mdc.module.getModule('MDCSTAT034_')['getList']($sel('#tboxisuSrtCd_finder_listisu0'));
                }
            

            return false;
          }
          //=/

          mdc.layer.openModal({
            appendTo: $content.getNode(),
            className: 'pop_opened pop_opened1',
            id: 'jsLayer_finder_listisu0',
            title: '상장 종목 검색',
            width: 548,
            height: 'auto',
            url: '/comm/finder/finder_listisu.jsp',
            useCloseButton: false,
            ajaxOption: {data: params},
            focus: $(this),
            afterAppend: function () {
              api.module.getModule('FINDER_LAYER__finder_listisu0').procInit();
            }
          });
        }
      };

      
      
      var isEmptyCodeVal = false;
      $sel('#tboxisuSrtCd_finder_listisu0').on('keyup', function (e) {
        if ( e.keyCode != 13 && !isEmptyCodeVal) {
          $sel('#isuSrtCd_finder_listisu0').val("");
          $sel('#isuSrtCd_finder_listisu02').val("");
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

  $('#tboxisuSrtCd_finder_listisu0').autocomplete({
    'contextName' : 'finder_listisu',
    'bldPath' : '/dbms/comm/finder/finder_listisu_autocomplete',
    'viewCount' : 5,
    'submit' : function (li) {

      var shotCd = li.attr('data-tp');
      var fullCd = li.attr('data-cd');
      var codeNm = li.attr('data-nm');
      var mktNm = '';

      $('#codeNmisuSrtCd_finder_listisu0').val(li.attr('data-nm'));
      $('#isuSrtCd_finder_listisu0').val(li.attr('data-cd'));
      $('#isuSrtCd_finder_listisu02').val(li.attr('data-tp'));

      // 지수면 명칭만
      if ( 'ISU' === 'IDX' ) {
        $('#tboxisuSrtCd_finder_listisu0').val(li.attr('data-nm'));
      }
      // 회사면 발행기관 코드
      else if ( 'ISU' === 'COM' ) {
        $('#tboxisuSrtCd_finder_listisu0').val(li.attr('data-cd')+'/'+li.attr('data-nm'));
      }
      // 그외 코드/명칭
      else {
        $('#tboxisuSrtCd_finder_listisu0').val(li.attr('data-tp')+'/'+li.attr('data-nm'));
      }

      var input = {
        finderCd: 'finder_listisu',
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
<tr>
<th scope="row">정렬방법</th>
<td colspan="3">
<select class="selectbox" id="sortType" name="sortType"><option selected="" value="A">종목명</option><option value="I">업종별</option><option value="J">자본금</option><option value="D">지정자문인</option></select>
<span style="position:relative; top:6px">
<input id="detailSch_0" name="detailSch" type="checkbox" value="Y"/><label for="detailSch_0">상세검색</label>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__141525729',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="detailSch"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT034_')['showSearchBox']($(this));
        });
      

      
    }
  });
</script>
</span>
</td>
</tr>
<tr class="jsS1">
<th class="freak1" scope="col">업종명</th>
<td class="jsDetailList jsInd">
<select class="selectbox" id="stdIndCd" name="stdIndCd"></select>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__141525730',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="stdIndCd"]');

      
      var params = {
        baseName: 'krx.mdc.i18n.component',
        key: 'B66.bld'
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
            if (option[0] === 'ALL') $option.prop('selected', true);
            $element.append($option);
          });
        }
      });
      

      

      
    }
  });
</script>
</td>
<th class="jsS2 freak1" scope="col">소속부</th>
<td class="jsS2 jsDetailList">
<select class="selectbox" id="sectTpCd" name="sectTpCd"></select>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__141525731',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="sectTpCd"]');

      
      var params = {
        baseName: 'krx.mdc.i18n.component',
        key: 'B153.bld'
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
<tr class="jsS1">
<th class="freak1" scope="col">액면가</th>
<td class="jsDetailList">
<select class="selectbox" id="parval" name="parval"><option selected="" value="ALL">전체</option><option value="1">10,000</option><option value="2">5,000</option><option value="3">2,500</option><option value="4">1,000</option><option value="5">500</option><option value="6">200</option><option value="7">100</option><option value="8">무액면</option><option value="9">기타</option></select>
</td>
<th class="freak1" scope="col">시가총액</th>
<td class="jsDetailList">
<select class="selectbox" id="mktcap" name="mktcap"><option selected="" value="ALL">전체</option><option value="1">10조 이상</option><option value="2">10조 ~ 5조</option><option value="3">5조 ~ 2조</option><option value="4">2조 ~ 1조</option><option value="5">1조 ~ 5,000억</option><option value="6">5,000억 ~ 3,000억</option><option value="7">3,000억 ~ 1,000억</option><option value="8">1,000억 ~ 500억</option><option value="9">500억 ~ 300억</option><option value="10">300억 ~ 100억</option><option value="11">100억 미만</option></select>
</td>
</tr>
<tr class="jsS1">
<th class="freak1" scope="col">결산월</th>
<td class="jsDetailList jsSearch6" colspan="3">
<select class="selectbox" id="acntclsMm" name="acntclsMm"><option selected="" value="ALL">전체</option><option value="1">12월</option><option value="2">9월</option><option value="3">6월</option><option value="4">3월</option><option value="5">기타</option></select>
</td>
<th class="jsS3 freak1" scope="col">지정자문인</th>
<td class="jsS3 jsDetailList">
<div class="searchBoxWrap">
<div class="search">
<p>
<input autocomplete="off" id="tboxmktpartcNo_finder_designadvser0" name="tboxmktpartcNo_finder_designadvser0" readonly="" style="width: 200px;" title="지정자문인 검색" type="text" value=""/>
<img alt="검색팝업" id="btnmktpartcNo_finder_designadvser0" name="btnmktpartcNo_finder_designadvser0" src="/pub/img/btn_dbg.png"/>
</p>
</div>
</div>
<input id="mktpartcNo_finder_designadvser0" name="mktpartcNo" type="hidden" value="">
<input id="mktpartcNo_finder_designadvser02" name="mktpartcNo2" type="hidden" value="">
<input id="codeNmmktpartcNo_finder_designadvser0" name="codeNmmktpartcNo_finder_designadvser0" type="hidden" value=""/>
<input id="param1mktpartcNo_finder_designadvser0" name="param1mktpartcNo_finder_designadvser0" type="hidden" value=""/>
<input id="" name="" type="hidden" value=""/>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'FINDER_COMPONENT_mktpartcNo_finder_designadvser0',
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
            if(cookie.codeVal)$sel('#mktpartcNo_finder_designadvser0').val(cookie.codeVal);
            if(cookie.tbox)$sel('#tboxmktpartcNo_finder_designadvser0').val(cookie.tbox);
            if(cookie.codeNm)$sel('#codeNmmktpartcNo_finder_designadvser0').val(cookie.codeNm);
            if(cookie.codeVal2)$sel('#mktpartcNo_finder_designadvser02').val(cookie.codeVal2);

            
          }
        }

        
      };

      

      $sel('#btnmktpartcNo_finder_designadvser0').on('click', function () {

        if($sel('#tboxmktpartcNo_finder_designadvser0').val()==""){
          self.openFinder(false);
        }else{
          self.openFinder(true);
        }

      });

      $sel('#tboxmktpartcNo_finder_designadvser0').on('keydown', function (e) {
        if (13 == e.keyCode) {
          if($sel('#tboxmktpartcNo_finder_designadvser0').val()==""){
            self.openFinder(false);
          }else{
            self.openFinder(true);
          }

        }
      });

      //쿠키 중복 방지
      self.getCookieFinderCd = function(){
        var cookieFinderCd = '';
        var curFinderCd = 'finder_designadvser';
        if(curFinderCd === 'finder_secuprodisu'){
          cookieFinderCd = 'finder_designadvser0';
        }
        else {
          cookieFinderCd = 'finder_designadvser';
        }
        return cookieFinderCd;
      };

      self.openFinder = function (isKeyDown) {
        var s_tboxNmVal = '';

        //캐쉬가 false/true선택관계없이 사용자가 검색어 입력시 그 값을 종목검색 팝업창에 전달
          var cookieFinderCd = self.getCookieFinderCd();
          var cookieFinderCdVal = api.util.getCookie(cookieFinderCd+'_finderCd');

            //검색텍스트박스값이 쿠키의 값과 같을경우 검색어 안넘어가도록
            var s_defaultVal = '';
            var s_tbox = api.util.getCookie(self.getCookieFinderCd()+'_tbox');

            if(s_tbox !== $sel('#tboxmktpartcNo_finder_designadvser0').val() && s_defaultVal !== $sel('#tboxmktpartcNo_finder_designadvser0').val()){
              s_tboxNmVal = $sel('#tboxmktpartcNo_finder_designadvser0').val();
            }

        var params = {
          finderNo: '_finder_designadvser0',
          finderCd: 'finder_designadvser',
          typeNo: '0',
          compValue: '',
          param1 : $sel('#param1mktpartcNo_finder_designadvser0').val(),
          tboxId : 'tboxmktpartcNo_finder_designadvser0',
          tboxNm : s_tboxNmVal,
          codeValId : 'mktpartcNo_finder_designadvser0',
          codeNmId : 'codeNmmktpartcNo_finder_designadvser0',
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

            

            return false;
          }
          //=/

          mdc.layer.openModal({
            appendTo: $content.getNode(),
            className: 'pop_opened pop_opened1',
            id: 'jsLayer_finder_designadvser0',
            title: '지정자문인 검색',
            width: 548,
            height: 'auto',
            url: '/comm/finder/finder_designadvser.jsp',
            useCloseButton: false,
            ajaxOption: {data: params},
            focus: $(this),
            afterAppend: function () {
              api.module.getModule('FINDER_LAYER__finder_designadvser0').procInit();
            }
          });
        }
      };

      
    }
  });



  
</script>
</input></input></td>
</tr>
<tr class="jsS1">
<th class="freak1" scope="col">상장주식수</th>
<td class="jsDetailList" colspan="3">
<select class="selectbox jsChgSelect" id="condListShrs" name="condListShrs"><option value="1">이상</option><option value="2">이하</option><option value="3">범위</option></select>
<input class="jsHide jsStart rangeStart" id="listshrs" name="listshrs" style="width: 100px;" type="text" value=""/>
<span class="jsHide">~</span>
<input class="jsHide jsEnd rangeEnd" id="listshrs2" name="listshrs2" style="width: 100px;" type="text" value=""/>
</td>
</tr>
<tr class="jsS1">
<th class="freak1" scope="col">자본금</th>
<td class="jsDetailList" colspan="3">
<select class="selectbox jsChgSelect" id="condCap" name="condCap"><option value="1">이상</option><option value="2">이하</option><option value="3">범위</option></select>
<input class="jsHide jsStart rangeStart" id="cap" name="cap" style="width: 100px;" type="text" value=""/>
<span class="jsHide">~</span>
<input class="jsHide jsEnd rangeEnd" id="cap2" name="cap2" style="width: 100px;" type="text" value=""/>
</td>
</tr>
</tbody>
</table>
<a class="btn_black btn_component_search" href="javascript:void(0);" id="jsSearchButton" name="search">조회</a>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'SEARCH_COMPONENT__141525738',
    mdi: {
      name: mdc.module.getMdiModuleName()
    },
    function: function (self, api) {
      var $content = api.getModuleNode();
      var $element = $content.select('[name="search"]');

      

      

      
        $element.on('click', function () {
          mdc.module.getModule('MDCSTAT034_')['getList']($(this));
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
<div class="sample_tb type4 mt10 mb10" id="jsOptionTable">
<table>
<colgroup>
<col style="width:13%;"/>
<col style="width:20%;"/>
<col style="width:13%;"/>
<col style="width:20%;"/>
<col style="width:11%;"/>
<col/>
</colgroup>
<tbody>
<tr>
<th class="pl0 tac" scope="col">전체상장기업</th>
<td class="pr10 tar"><span data-bind="ISUR_CNT" name="ISUR_CNT"></span> 개사</td>
<th class="pl0 tac" scope="col">전체상장종목</th>
<td class="pr10 tar"><span data-bind="ISU_CNT" name="ISU_CNT"></span> 종목</td>
<th class="pl0 tac" scope="col">검색결과</th>
<td class="pr10 tar"><span data-bind="TOT_CNT" name="TOT_CNT"></span> 개</td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT034_0">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="REP_ISU_SRT_CD" scope="col" width="80px">종목코드</th>
<th name="COM_ABBRV" scope="col" width="150px">종목명</th>
<th align="center" name="MKT_NM" scope="col" width="80px">시장구분</th>
<th align="left" name="SECT_TP_NM" scope="col" width="140px">소속부</th>
<th align="center" name="STD_IND_CD" scope="col" width="80px">업종코드</th>
<th name="IND_NM" scope="col" width="300px">업종명</th>
<th align="center" name="ACNTCLS_MM" scope="col" width="70px">결산월</th>
<th align="center" name="MKTPARTC_NM" scope="col" width="120px">지정자문인</th>
<th align="right" name="LIST_SHRS" scope="col" width="90px">상장주식수</th>
<th align="right" name="PARVAL" scope="col" width="65px">액면가</th>
<th align="right" name="CAP" scope="col" width="130px">자본금</th>
<th align="center" name="ISO_CD" scope="col" width="80px">통화구분</th>
<th name="CEO_NM" scope="col" width="200px">대표이사</th>
<th align="center" name="TEL_NO" scope="col" width="110px">대표전화</th>
<th name="ADDR" scope="col" width="400px">주소</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="REP_ISU_SRT_CD" name="REP_ISU_SRT_CD"></td>
<td bind="COM_ABBRV" name="COM_ABBRV"></td>
<td bind="MKT_NM" name="MKT_NM"></td>
<td bind="SECT_TP_NM" name="SECT_TP_NM"></td>
<td bind="STD_IND_CD" name="STD_IND_CD"></td>
<td bind="IND_NM" name="IND_NM"></td>
<td bind="ACNTCLS_MM" name="ACNTCLS_MM"></td>
<td bind="MKTPARTC_NM" name="MKTPARTC_NM"></td>
<td bind="LIST_SHRS" name="LIST_SHRS"></td>
<td bind="PARVAL" name="PARVAL"></td>
<td bind="CAP" name="CAP"></td>
<td bind="ISO_CD" name="ISO_CD"></td>
<td bind="CEO_NM" name="CEO_NM"></td>
<td bind="TEL_NO" name="TEL_NO"></td>
<td bind="ADDR" name="ADDR"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT034_1">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="REP_ISU_SRT_CD" scope="col" width="80px">종목코드</th>
<th name="COM_ABBRV" scope="col" width="140px">종목명</th>
<th align="center" name="STD_IND_CD" scope="col" width="80px">업종코드</th>
<th name="IND_NM" scope="col" width="300px">업종명</th>
<th align="center" name="ACNTCLS_MM" scope="col" width="70px">결산월</th>
<th align="right" name="LIST_SHRS" scope="col" width="90px">상장주식수</th>
<th align="right" name="PARVAL" scope="col" width="65px">액면가</th>
<th align="right" name="CAP" scope="col" width="130px">자본금</th>
<th align="center" name="ISO_CD" scope="col" width="80px">통화구분</th>
<th name="CEO_NM" scope="col" width="200px">대표이사</th>
<th align="center" name="TEL_NO" scope="col" width="110px">대표전화</th>
<th name="ADDR" scope="col" width="400px">주소</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="REP_ISU_SRT_CD" name="REP_ISU_SRT_CD"></td>
<td bind="COM_ABBRV" name="COM_ABBRV"></td>
<td bind="STD_IND_CD" name="STD_IND_CD"></td>
<td bind="IND_NM" name="IND_NM"></td>
<td bind="ACNTCLS_MM" name="ACNTCLS_MM"></td>
<td bind="LIST_SHRS" name="LIST_SHRS"></td>
<td bind="PARVAL" name="PARVAL"></td>
<td bind="CAP" name="CAP"></td>
<td bind="ISO_CD" name="ISO_CD"></td>
<td bind="CEO_NM" name="CEO_NM"></td>
<td bind="TEL_NO" name="TEL_NO"></td>
<td bind="ADDR" name="ADDR"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT034_2">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="REP_ISU_SRT_CD" scope="col" width="80px">종목코드</th>
<th name="COM_ABBRV" scope="col" width="140px">종목명</th>
<th align="left" name="SECT_TP_NM" scope="col" width="140px">소속부</th>
<th align="left" name="SUB_IDX_IND_NM" scope="col" width="160px">기술성장기업부 유형</th>
<th align="center" name="STD_IND_CD" scope="col" width="80px">업종코드</th>
<th name="IND_NM" scope="col" width="300px">업종명</th>
<th align="center" name="ACNTCLS_MM" scope="col" width="70px">결산월</th>
<th align="right" name="LIST_SHRS" scope="col" width="90px">상장주식수</th>
<th align="right" name="PARVAL" scope="col" width="65px">액면가</th>
<th align="right" name="CAP" scope="col" width="130px">자본금</th>
<th align="center" name="ISO_CD" scope="col" width="80px">통화구분</th>
<th name="CEO_NM" scope="col" width="200px">대표이사</th>
<th align="center" name="TEL_NO" scope="col" width="110px">대표전화</th>
<th name="ADDR" scope="col" width="400px">주소</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="REP_ISU_SRT_CD" name="REP_ISU_SRT_CD"></td>
<td bind="COM_ABBRV" name="COM_ABBRV"></td>
<td bind="SECT_TP_NM" name="SECT_TP_NM"></td>
<td bind="SUB_IDX_IND_NM" name="SUB_IDX_IND_NM"></td>
<td bind="STD_IND_CD" name="STD_IND_CD"></td>
<td bind="IND_NM" name="IND_NM"></td>
<td bind="ACNTCLS_MM" name="ACNTCLS_MM"></td>
<td bind="LIST_SHRS" name="LIST_SHRS"></td>
<td bind="PARVAL" name="PARVAL"></td>
<td bind="CAP" name="CAP"></td>
<td bind="ISO_CD" name="ISO_CD"></td>
<td bind="CEO_NM" name="CEO_NM"></td>
<td bind="TEL_NO" name="TEL_NO"></td>
<td bind="ADDR" name="ADDR"></td>
</tr>
</tbody>
</table>
</div>
<div id="jsGrid_MDCSTAT034_3">
<table>
<thead>
<tr>
<th align="center" data-sorttype="string" name="REP_ISU_SRT_CD" scope="col" width="80px">종목코드</th>
<th name="COM_ABBRV" scope="col" width="150px">종목명</th>
<th align="left" name="SECT_TP_NM" scope="col" width="140px">소속부</th>
<th align="center" name="STD_IND_CD" scope="col" width="80px">업종코드</th>
<th name="IND_NM" scope="col" width="300px">업종명</th>
<th align="center" name="ACNTCLS_MM" scope="col" width="70px">결산월</th>
<th align="center" name="MKTPARTC_NM" scope="col" width="120px">지정자문인</th>
<th align="right" name="LIST_SHRS" scope="col" width="90px">상장주식수</th>
<th align="right" name="PARVAL" scope="col" width="65px">액면가</th>
<th align="right" name="CAP" scope="col" width="130px">자본금</th>
<th align="center" name="ISO_CD" scope="col" width="80px">통화구분</th>
<th name="CEO_NM" scope="col" width="200px">대표이사</th>
<th align="center" name="TEL_NO" scope="col" width="110px">대표전화</th>
<th name="ADDR" scope="col" width="400px">주소</th>
</tr>
</thead>
<tbody>
<tr>
<td bind="REP_ISU_SRT_CD" name="REP_ISU_SRT_CD"></td>
<td bind="COM_ABBRV" name="COM_ABBRV"></td>
<td bind="SECT_TP_NM" name="SECT_TP_NM"></td>
<td bind="STD_IND_CD" name="STD_IND_CD"></td>
<td bind="IND_NM" name="IND_NM"></td>
<td bind="ACNTCLS_MM" name="ACNTCLS_MM"></td>
<td bind="MKTPARTC_NM" name="MKTPARTC_NM"></td>
<td bind="LIST_SHRS" name="LIST_SHRS"></td>
<td bind="PARVAL" name="PARVAL"></td>
<td bind="CAP" name="CAP"></td>
<td bind="ISO_CD" name="ISO_CD"></td>
<td bind="CEO_NM" name="CEO_NM"></td>
<td bind="TEL_NO" name="TEL_NO"></td>
<td bind="ADDR" name="ADDR"></td>
</tr>
</tbody>
</table>
</div>
<div class="result_bottom CI-MDI-COMPONENT-FOOTER on2">
<button class="CI-MDI-COMPONENT-BUTTON" type="button">Open</button>
<div data-component="footer" style="display: none;">
<span><dfn>컨텐츠 문의</dfn> : (유)주식시장부,  (코)코스닥시장부,  (넥)코넥스시장부,  고객센터 (1577-0088)</span>
<p><img alt="" src="/templets/mdc/img/blit_feel.png"/> 본 정보는 투자참고 사항이며, 오류가 발생하거나 지연될 수 있습니다. 제공된 정보에 의한 투자결과에 대한 법적인 책임을 지지 않습니다.</p>
</div>
</div>
<script type="text/javascript">
  mdc.module.setModule({
    name: 'MDCSTAT034_',
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
      var $f = $content.select('#MDCSTAT034_FORM');

      self.resizeGrid = function (e) {
        self.grid.setHeight(e.getContentLeftHeight() - $('#jsOptionTable').innerHeight() - 16);
        self.grid.resize();
      };

      self.init = function () {
        self.grid = api.util.grid.init({
          node: api.getModuleNode().getNode(),
          form: $f,
          layout: 'no-apply',
          grid: [
            {
              template: $content.select('#jsGrid_MDCSTAT034_0'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03402',
              bldDataKey: 'block1',
              lateInfoYn: false,
              unit: {
                share: ['LIST_SHRS'],
                money: ['CAP']
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT034_1'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03402',
              bldDataKey: 'block1',
              lateInfoYn: false,
              unit: {
                share: ['LIST_SHRS'],
                money: ['CAP']
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT034_2'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03402',
              bldDataKey: 'block1',
              lateInfoYn: false,
              unit: {
                share: ['LIST_SHRS'],
                money: ['CAP']
              }
            },
            {
              template: $content.select('#jsGrid_MDCSTAT034_3'),
              bld: 'dbms/MDC/STAT/standard/MDCSTAT03402',
              bldDataKey: 'block1',
              lateInfoYn: false,
              unit: {
                share: ['LIST_SHRS'],
                money: ['CAP']
              }
            }
          ]
        });

        var $jsDetailList = $f.find(".jsDetailList");

        $jsDetailList.each(function() {
          var $this = $(this);
          var thisName = $this.children('input').attr("name");
          var thisText = $this.prev("th").text();
          $this.prev("th").html('');
          if (thisName === undefined) {
            thisName = $this.children('select').prop("name");
          }
          var $inputBox = $('<input />', {
            id: 'ck' + thisName.replace(/^./, thisName[0].toUpperCase()),
            type: 'checkbox',
            name: 'ck' + thisName.replace(/^./, thisName[0].toUpperCase()),
            value: 'Y',
            class: 'js_' + $this.children('select').prop("name")
          });
          var $chkBox =$('<label />', {
            for: 'ck' + thisName.replace(/^./, thisName[0].toUpperCase())
          }).append(thisText);

          $this.prev("th").append($inputBox).append($chkBox);
        });

        //= (20201211, 김정삼)
        $('select', $jsDetailList).on('change', function () {
          var $this = $(this);
          var ckbClass = 'js_' + $this.prop("name");
          $this.closest('tr').find('.' + ckbClass).prop('checked', true);
        });
        //=/

        $f.find('.jsS1').hide();
        $f.find('.jsS2').show();
        $f.find('.jsS3').hide();
        $f.find('.jsHide').hide();
        $f.find('#listshrs').show();
        $f.find('#cap').show();
        $f.find('#sortType option[value="D"]').css('display','none');

        self.getList();

      };

      self.chgMktId = function () {
        var value = $f.find('[name="mktTpCd"]:checked').val();
        if (value === '0' || value === '1') {
          if ( value === '1' ) {
            $f.find('.jsS2').hide();
          } else {
            $f.find('.jsS2').show();
            api.util.makeBldSelectBox($f, 'sectTpCd', 'dbms/comm/component/sectTpCombo');
          }
          $f.find('.jsS3').hide();
          $f.find('[name="ckStdIndCd"]').attr("checked", false);
          $f.find('[name="ckMktpartcNo"]').attr("checked", false);
//          $f.find('.jsInd').attr('colspan','3');
          $f.find('.jsSearch6').attr('colspan','3');
          $f.find('#sortType option[value="D"]').css('display','none');
        } else if (value === '2') {
          $f.find('.jsS2').show();
          api.util.makeBldSelectBox($f, 'sectTpCd', 'dbms/comm/component/sectTpCombo');
          $f.find('.jsS3').hide();
          $f.find('[name="ckMktpartcNo"]').attr("checked", false);
//          $f.find('.jsInd').attr('colspan','1');
          $f.find('.jsSearch6').attr('colspan','3');
          $f.find('#sortType option[value="D"]').css('display','none');
        } else if (value === '6') {
          $f.find('.jsS2').show();
          api.util.makeBldSelectBox($f, 'sectTpCd', 'dbms/comm/component/sectTpCombo');
          $f.find('.jsS3').show();
//          $f.find('.jsInd').attr('colspan','1');
          $f.find('.jsSearch6').attr('colspan','1');
          $f.find('#sortType option[value="D"]').css('display','block');
        }
      };

      self.showSearchBox = function () {
        var value = $f.find('[name="detailSch"]').is(':checked');
        if (value === true) {
          $f.find('.jsS1').show();
        } else {
          $f.find('.jsS1').hide();
        }
        self.grid.setHeight(mdc.module.getModule('MDI_MODULE')["_MDC_MDI_OBJECT"].getContentLeftHeight($content.getNode()) - $('#jsOptionTable').innerHeight() - 16);
        self.grid.resize();
      };

      self.getList = function () {
        var value = $f.find('[name="mktTpCd"]:checked').val();
        var index = 0;
        if (value === '1') { index = 1; }
        else if (value === '2') { index = 2; }
        else if (value === '6') { index = 3; }

        self.grid.setIndex(index);
        self.grid.show();
        self.grid.appendRow();
        self.grid.resize();

        api.util.submitAjax({
          url: '/comm/bldAttendant/getJsonData.cmd?bld=dbms/MDC/STAT/standard/MDCSTAT03401',
          data: $f.serialize(),
          async: false,
          success: function (data) {
            mdc.util.singleDatabind($content.select('#jsOptionTable'), data['block1'][0]);
            // orderColumnData = data['block1'];
          }
        });
      };


      $f.find('.jsChgSelect').on('change', function () {
        var value = $(this).val();
        $(this).parent().find('.jsHide').hide();
        if (value === '1'){
          $(this).parent().children('.jsStart').show();
        } else if (value === '2'){
          $(this).parent().children('.jsEnd').show();
        } else {
          $(this).parent().children('.jsStart').show();
          $(this).parent().children('.jsEnd').show();
          $(this).parent().children('span').show();
        }
      });

    }
  });
</script>
