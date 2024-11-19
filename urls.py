from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    
    
    path('home_alemgena/', views.alemgena_home, name="home_alemgena"),
    path('alemgena_hamle/', views.alemgenahamle, name="alemgena_hamle"),
    path('alemgena_nehase/', views.alemgenanehase, name="alemgena_nehase"),
    path('alemgena_sep/', views.alemgenasep, name="alemgena_sep"),
    path('alemgena_oct/', views.alemgenaoct, name="alemgena_oct"),
    path('alemgena_nov/', views.alemgenanov, name="alemgena_nov"),
    path('alemgena_dec/', views.alemgenadec, name="alemgena_dec"),
    path('alemgena_jan/', views.alemgenajan, name="alemgena_jan"),
    path('alemgena_feb/', views.alemgenafeb, name="alemgena_feb"),
    path('alemgena_mar/', views.alemgenamar, name="alemgena_mar"),
    path('alemgena_apr/', views.alemgenaapr, name="alemgena_apr"),
    path('alemgena_may/', views.alemgenamay, name="alemgena_may"),
    path('alemgena_jun/', views.alemgenajun, name="alemgena_jun"),
    path('home_adigrat/', views.adigrat_home, name="home_adigrat"),
    path('home_kombolcha/', views.kombolcha_home, name="home_kombolcha"),
    path('home_debremarkos/', views.debremarkos_home, name="home_debremarkos"),
    path('home_gondar/', views.gondar_home, name="home_gondar"),
    path('home_shashamane/', views.shashamane_home, name="home_shashamane"),
    path('home_nekemte/', views.nekemte_home, name="home_nekemte"),
    path('home_diredawa/', views.diredawa_home, name="home_diredawa"),
    path('home_jimma/', views.jimma_home, name="home_jimma"),
    path('home_sodo/', views.sodo_home, name="home_sodo"),
    path('home_gode/', views.gode_home, name="home_gode"),
    
    
    
    path('', views.Home, name="home"),
    path('user/', views.userPage, name="user-page"),
    path('getuser/', views.get_username),
    
    path('dashboard', views.rams_dashboard, name="dashboard"),
    path('budgetext/<str:pk>/', views.budgetext, name="budgetext"),
    path('budget_list/', views.budgetList, name="budget_list"),
    path('budget/', views.budget),
    path('bactionplan/', views.budgetedap, name='bactionplan'),
    
    
    path('filterbapacoml/', views.bapacoml, name='filterbapacoml'),
    

    
    path('alemgena/', views.districtalemgena, name="alemgena"),
    path('adigratl/', views.districtadigrat, name="adigratl"),
    path('kombolchal/', views.districtkombolcha, name="kombolchal"),
    path('debremarkosl/', views.districtdebremarkos, name="debremarkosl"),
    path('gondarl/', views.districtgondar, name="gondarl"),
    path('shashamanel/', views.districtshashamane, name="shashamanel"),
    path('nekemte/', views.districtnekemte, name="nekemte"),
    path('diredawal/', views.districtdiredawa, name="diredawal"),
    path('jimmal/', views.districtjimma, name="jimmal"),
    path('sodol/', views.districtsodo, name="sodol"),
    path('godel/', views.districtgode, name="godel"),
    
    
    
    path('branch_summary/', views.rambranch_summary, name="branch_summary"),
    path('district_apaccomp_compfirstm/', views.district_compare_firstmonth, name="district_apaccomp_compfirstm"),
    path('district_apaccomp_compsecond/', views.district_compare_second, name="district_apaccomp_compsecond"),
    path('district_apaccomp_compthird/', views.district_compare_third, name="district_apaccomp_compthird"),
    path('district_apaccomp_compfourth/', views.district_compare_fourth, name="district_apaccomp_compfourth"),
    path('district_apaccomp_compfifth/', views.district_compare_fifth, name="district_apaccomp_compfifth"),
    path('district_apaccomp_compsixth/', views.district_compare_sixth, name="district_apaccomp_compsixth"),
    path('district_apaccomp_compseventh/', views.district_compare_seventh, name="district_apaccomp_compseventh"),
    path('district_apaccomp_compeighth/', views.district_compare_eighth, name="district_apaccomp_compeighth"),
    path('district_apaccomp_compnineth/', views.district_compare_nineth, name="district_apaccomp_compnineth"),
    path('district_apaccomp_comptenth/', views.district_compare_tenth, name="district_apaccomp_comptenth"),
    path('district_apaccomp_compelvnth/', views.district_compare_elvm, name="district_apaccomp_compelvnth"),
    path('district_apaccomp_compyr/', views.district_compare_yr, name="district_apaccomp_compyr"),
    path('sample/', views.apaccomp_per_district, name="sample"),
    
    path('ownfbranch_summary/', views.ownfbranch_summary, name="ownfbranch_summary"),
    path('ownf_dist_apacompcomp_firstm/', views.ownf_district_comp_first, name="ownf_dist_apacompcomp_firstm"),
    path('ownf_dist_apacompcomp_twom/', views.ownf_district_comp_second, name="ownf_dist_apacompcomp_twom"),
    path('ownf_dist_apacompcomp_threem/', views.ownf_district_comp_third, name="ownf_dist_apacompcomp_threem"),
    path('ownf_dist_apacompcomp_fourm/', views.ownf_district_comp_fourth, name="ownf_dist_apacompcomp_fourm"),
    path('ownf_dist_apacompcomp_fivem/', views.ownf_district_comp_fifth, name="ownf_dist_apacompcomp_fivem"),
    path('ownf_dist_apacompcomp_sixm/', views.ownf_district_comp_sixth, name="ownf_dist_apacompcomp_sixm"),
    path('ownf_dist_apacompcomp_sevenm/', views.ownf_district_comp_seventh, name="ownf_dist_apacompcomp_sevenm"),
    path('ownf_dist_apacompcomp_eightm/', views.ownf_district_comp_eighth, name="ownf_dist_apacompcomp_eightm"),
    path('ownf_dist_apacompcomp_ninem/', views.ownf_district_comp_nineth, name="ownf_dist_apacompcomp_ninem"),
    path('ownf_dist_apacompcomp_tenm/', views.ownf_district_comp_tenth, name="ownf_dist_apacompcomp_tenm"),
    path('ownforce_district_apacompcomp/', views.ownf_district_comp, name="ownforce_district_apacompcomp"),
    path('ownforce_district_apacompcompyr/', views.ownf_district_compyr, name="ownforce_district_apacompcompyr"),
    
    path('contractor_apacompcomp_one/', views.contractor_apacompcomp_one, name="contractor_apacompcomp_one"),
    path('contractor_apacompcomp_two/', views.contractor_apacompcomp_two, name="contractor_apacompcomp_two"),
    path('contractor_apacompcomp_three/', views.contractor_apacompcomp_three, name="contractor_apacompcomp_three"),
    path('contractor_apacompcomp_four/', views.contractor_apacompcomp_four, name="contractor_apacompcomp_four"),
    path('contractor_apacompcomp_five/', views.contractor_apacompcomp_five, name="contractor_apacompcomp_five"),
    path('contractor_apacompcomp_six/', views.contractor_apacompcomp_six, name="contractor_apacompcomp_six"),
    path('contractor_apacompcomp_seven/', views.contractor_apacompcomp_seven, name="contractor_apacompcomp_seven"),
    path('contractor_apacompcomp_eight/', views.contractor_apacompcomp_eight, name="contractor_apacompcomp_eight"),
    path('contractor_apacompcomp_nine/', views.contractor_apacompcomp_nine, name="contractor_apacompcomp_nine"),
    path('contractor_apacompcomp_ten/', views.contractor_apacompcomp_ten, name="contractor_apacompcomp_ten"),
    path('contractor_apacompcomp_eleven/', views.contractor_apacompcomp_eleven, name="contractor_apacompcomp_eleven"),
    path('contractor_apacompcomp_yr/', views.contractor_apacompcomp_yr, name="contractor_apacompcomp_yr"),
    path('contractor_apacompcomp/', views.contractor_comp, name="contractor_apacompcomp"),

    path('intervention_summary/', views.intervention_summary, name="intervention_summary"),
    path('intervention_apacompcomp_first/', views.intervention_summary_firstm, name="intervention_apacompcomp_first"),
    path('intervention_apacompcomp_second/', views.intervention_summary_secondm, name="intervention_apacompcomp_second"),
    path('intervention_apacompcomp_three/', views.intervention_summary_thirdm, name="intervention_apacompcomp_three"),
    path('intervention_apacompcomp_four/', views.intervention_summary_fourthm, name="intervention_apacompcomp_four"),
    path('intervention_apacompcomp_five/', views.intervention_summary_fifthm, name="intervention_apacompcomp_five"),
    path('intervention_apacompcomp_six/', views.intervention_summary_sixthm, name="intervention_apacompcomp_six"),
    path('intervention_apacompcomp_seven/', views.intervention_summary_seventhm, name="intervention_apacompcomp_seven"),
    path('intervention_apacompcomp_eight/', views.intervention_summary_eighthm, name="intervention_apacompcomp_eight"),
    path('intervention_apacompcomp_nine/', views.intervention_summary_ninthm, name="intervention_apacompcomp_nine"),
    path('intervention_apacompcomp_ten/', views.intervention_summary_tenthm, name="intervention_apacompcomp_ten"),
    path('intervention_apacompcomp_eleven/', views.intervention_summary_eleventhm, name="intervention_apacompcomp_eleven"),
    path('intervention_apacompcomp_yr/', views.intervention_summary_yr, name="intervention_apacompcomp_yr"),
    

    path('allbyprojectfirst/', views.allbyproject_first, name="allbyprojectfirst"),
    path('allbyprojectsecond/', views.allbyproject_second, name="allbyprojectsecond"),
    path('allbyprojectthird/', views.allbyproject_third, name="allbyprojectthird"),
    path('allbyprojectfourth/', views.allbyproject_fourth, name="allbyprojectfourth"),
    path('allbyprojectfifth/', views.allbyproject_fifth, name="allbyprojectfifth"),
    path('allbyprojectsixth/', views.allbyproject_sixth, name="allbyprojectsixth"),
    path('allbyprojectseventh/', views.allbyproject_seventh, name="allbyprojectseventh"),
    path('allbyprojecteighth/', views.allbyproject_eighth, name="allbyprojecteighth"),
    path('allbyprojectnineth/', views.allbyproject_nineth, name="allbyprojectnineth"),
    path('allbyprojecttenth/', views.allbyproject_tenth, name="allbyprojecttenth"),
    path('allbyprojecteleventh/', views.allbyproject_eleventh, name="allbyprojecteleventh"),
    path('allbyproject_yr/', views.allbyproject_yr, name="allbyproject_yr"),



    path('financer_apaccomp_compyr/', views.financer_compare_yr, name="financer_apaccomp_compyr"),


    
    path('all_byprojsummary/', views.all_by_project_summary, name="all_byprojsummary"),

    path('alldistrict/<int:pk>/', views.districtAll, name="alldistrict"),
    path('groupbudget/', views.budgetsummary, name="groupbudget"),
    path('budgetsummary/', views.summarydata, name="budgetsummary"),
    path('annualbudget/', views.AnnualBudgetS, name="annualbudget"),
    path('roadsummary/', views.roadtypesummary, name="roadsummary"),
    path('create_actionplan/<str:pk>/', views.createActionPlan, name="create_actionplan"),
    path('update_actionplan/<str:pk>/', views.updateActionPlan, name="update_actionplan"),
    path('delete_actionplan/<str:pk>/', views.deleteActionPlan, name="delete_actionplan"),
    
    
    path('bapdetail/', views.bactionp, name='bapdetail'),
    path('bapalemgena/', views.bactionpalemgena, name='bapalemgena'),
    path('bapladigrat/', views.bactionpadigrat, name='bapladigrat'),
    path('bapkombolcha/', views.bactionpkombolcha, name='bapkombolcha'),
    path('bapdebremarkos/', views.bactionpdebremarkos, name='bapdebremarkos'),
    path('bapgondar/', views.bactionpgondar, name='bapgondar'),
    path('bapshashamane/', views.bactionpshashamane, name='bapshashamane'),
    path('bapnekemte/', views.bactionpnekemte, name='bapnekemte'),
    path('bapdiredawa/', views.bactionpdiredawa, name='bapdiredawa'),
    path('bapjimma/', views.bactionpjimma, name='bapjimma'),
    path('bapsodo/', views.bactionpsodo, name='bapsodo'),
    path('bapgode/', views.bactionpgode, name='bapgode'),
    
    
    path('accomplishl/', views.accomplist, name='accomplishl'),
    path('accomplishl_nehase/', views.accomplist_nehase, name='accomplishl_nehase'),
    path('accomplishl_sep/', views.accomplist_sep, name='accomplishl_sep'),
    path('accomplishl_oct/', views.accomplist_oct, name='accomplishl_oct'),
    path('accomplishl_nov/', views.accomplist_nov, name='accomplishl_nov'),
    path('accomplishl_dec/', views.accomplist_dec, name='accomplishl_dec'),
    path('accomplishl_jan/', views.accomplist_jan, name='accomplishl_jan'),
    path('accomplishl_feb/', views.accomplist_feb, name='accomplishl_feb'),
    path('accomplishl_mar/', views.accomplist_mar, name='accomplishl_mar'),
    path('accomplishl_apr/', views.accomplist_apr, name='accomplishl_apr'),
    path('accomplishl_may/', views.accomplist_may, name='accomplishl_may'),
    path('accomplishl_jun/', views.accomplist_jun, name='accomplishl_jun'),
    path('accomplishlist/', views.accomplishlist, name='accomplishlist'),
    path('accomplishladigrat/', views.accomplishlistadigrat, name='accomplishladigrat'),
    path('accomplishlalemgena/', views.accomplishlistalemgena, name='accomplishlalemgena'),
    path('accomplishlkombolcha/', views.accomplishlistkombolcha, name='accomplishlkombolcha'),
    path('accomplishldebremarkos/', views.accomplishlistdebremarkos, name='accomplishldebremarkos'),
    path('accomplishlgondar/', views.accomplishlistgondar, name='accomplishlgondar'),
    path('accomplishlshashamane/', views.accomplishlistshashamane, name='accomplishlshashamane'),
    path('accomplishlnekemte/', views.accomplishlistnekemte, name='accomplishlnekemte'),
    path('accomplishldiredawa/', views.accomplishlistdiredawa, name='accomplishldiredawa'),
    path('accomplishljimma/', views.accomplishlistjimma, name='accomplishljimma'),
    path('accomplishlsodo/', views.accomplishlistsodo, name='accomplishlsodo'),
    path('accomplishlgode/', views.accomplishlistgode, name='accomplishlgode'),
    
    path('apaccomplstalemgena/', views.ap_accomplishlistalemgena, name='apaccomplstalemgena'),
    
    path('maindashboard/', views.maindashboard, name="maindashboard"),

    
    path('exportx/<str:file_format>/', views.export_to_excel, name='export_to_excel'),
    path('csvexport/', views.export_to_csv, name='csvexport'),
    path('exportxls/', views.exportxl, name='exportxls'),
    
    
    path('branchchart/', views.branchchart, name='branchchart'),
    path('roadl-branch-chart/', views.roadl_branch_chart, name='roadl-branch-chart'),
    path('apacompchartelvm/', views.apacompchartelvm, name='apacompchartelvm'),
    path('apacomp-elvm-chart/', views.apacomp_elvm_chart, name='apacomp-elvm-chart'),
    
    path('budgetexport/', views.bexport, name='budgetexport'),
    path('interventionsummaryexp/', views.intervention_summary_export, name='interventionsummaryexp'),
    
    path('apacomp_upd/', views.apacompupd, name='apacomp_upd'),
    path('accomplishmentnew/', views.accomplish_new, name='accomplishmentnew'),
    path('accomplish/<str:id>/', views.accomplishments, name='accomplish'),
    path('apsedit/', views.aps_edit, name='apsedit'),
    path('apsformset/', views.createaps, name="apsformset"),
    path('budgetpdispprojtype/', views.budgetperdisperprojtype, name="budgetpdispprojtype"),
    path('worktype_apaccomp/', views.worktypeperapnaccomp, name="worktype_apaccomp"),
    path('aplist/', views.ActionPlanList, name="aplist"),
    path('backtodistrict/', views.backtodis, name="backtodistrict"),
    
    
    path('accomplishment_reg/', views.accomplishment_update, name="accomplishment_reg"),
    path('adminaccomplish/', views.accomplishment_admin, name="adminaccomplish"),
    path('adigrataccompreg/', views.accomplishment_update_adigrat, name="adigrataccompreg"),
    path('kombolchaaccompreg/', views.accomplish_upd_kombolcha, name="kombolchaaccompreg"),
    path('debremarkosaccompreg/', views.accomplish_upd_debremarkos, name="debremarkosaccompreg"),
    path('gondaraccompreg/', views.accomplish_upd_gondar, name="gondaraccompreg"),
    path('shashamaneaccompreg/', views.accomplish_upd_shashamane, name="shashamaneaccompreg"),
    path('nekemteaccompreg/', views.accomplish_upd_nekemte, name="nekemteaccompreg"),
    path('diredawaaccompreg/', views.accomplish_upd_diredawa, name="diredawaaccompreg"),
    path('jimmaaccompreg/', views.accomplish_upd_jimma, name="jimmaaccompreg"),
    path('sodoaccompreg/', views.accomplish_upd_sodo, name="sodoaccompreg"),
    path('godeaccompreg/', views.accomplish_upd_gode, name="godeaccompreg"),
    path('search_example/', views.search_accomplish, name="search_example"),
    
    
    path('apaccomp_comp/', views.apaccompcomp, name="apaccomp_comp"),
    path('apaccomp_compscnd/', views.apaccompcompscnd, name="apaccomp_compscnd"),
    path('apaccomp_compthrd/', views.apaccompcompthrd, name="apaccomp_compthrd"),
    path('apaccomp_compfrth/', views.apaccompcompfrth, name="apaccomp_compfrth"),
    path('apaccomp_compffth/', views.apaccompcompffth, name="apaccomp_compffth"),
    path('apaccomp_compsixth/', views.apaccompcompsixth, name="apaccomp_compsixth"),
    path('apaccomp_compsevnth/', views.apaccompcompsevnth, name="apaccomp_compsevnth"),
    path('apaccomp_compeith/', views.apaccompcompeith, name="apaccomp_compeith"),
    path('apaccomp_compninth/', views.apaccompcompninth, name="apaccomp_compninth"),
    path('apaccomp_comptenth/', views.apaccompcomptenth, name="apaccomp_comptenth"),
    path('apaccomp_compelvnth/', views.apaccompcompelvnth, name="apaccomp_compelvnth"),
    path('apaccomp_complast/', views.apaccompcomplast, name="apaccomp_complast"),
    path('btemplate/', views.bsummary, name="btemplate"),
    path('fin_maintenance_summary/', views.finbsummary, name="fin_maintenance_summary"),
    path('yearlyapvsaccomp/', views.annualapvsaccomp, name="yearlyapvsaccomp"),
    path('apaccompcompare/', views.apaccomp_compare, name="apaccompcompare"),
    
    path('apwithaccomp_comparison/', views.apaccompcomparison, name="apwithaccomp_comparison"),
    path('disapwithaccomp_comparison/', views.disapaccompcomparison, name="disapwithaccomp_comparison"),
    path('owndisapwithaccomp_comparison/', views.ownfdisapaccompcomparison, name="owndisapwithaccomp_comparison"),
    path('contractor_apacmop_comparison/', views.contractor_comparison, name="contractor_apacmop_comparison"),
    path('intervention_apacmop_comparison/', views.intervention_comparison, name="intervention_apacmop_comparison"),
    
    
    # Added Paths
    path('about/', views.about, name="about"),
    path('quarterly_branchoffice/', views.quarterly_branchoffice, name="quarterly_branchoffice"),
    path('quarterly_byfinance/', views.quarterly_byfinance, name="quarterly_byfinance"),
    path('quarterly_byproject/', views.quarterly_byproject, name="quarterly_byproject"),
    path('quarterly_contractor/', views.quarterly_contractor, name="quarterly_contractor"),
    path('quarterly_intervention/', views.quarterly_intervention, name="quarterly_intervention"),
    path('quarterly_ownbranch/', views.quarterly_ownbranch, name="quarterly_ownbranch"),
    
    

    path('annual_branchoffice/', views.annual_branchoffice, name="annual_branchoffice"),
    path('annual_byfinancer/', views.annual_byfinancer, name="annual_byfinancer"),
    path('annual_byproject/', views.annual_byproject, name="annual_byproject"),
    path('annual_contractor/', views.annual_contractor, name="annual_contractor"),
    path('annual_intervention/', views.annual_intervention, name="annual_intervention"),
    path('annual_ownforce/', views.annual_ownforce, name="annual_ownforce"),

    # Ends here



    path('grouped/', views.grouped_items, name='grouped_items'),
    path('finwithcontractor/', views.financerwithcontractor, name='finwithcontractor'),
    path('financerpercontractor/', views.financerpercontractor, name='financerpercontractor'),
    path('budgetpworktype/', views.budgetperworktype, name='budgetpworktype'),
    path('byworktype/', views.summarybyworktype, name='byworktype'),
    path('acompbyworktype/', views.acompsummarybyworktype, name='acompbyworktype'),
    path('appprojectpmonth/', views.apperprojectpermonth, name='appprojectpmonth'),
    path('budgetpproject/', views.budgetperprojectype, name='bpproject'),
    path('budgetpprojectname/', views.budgetperprojectname, name='bpprojectname'),
    path('apcompacomplish/', views.apcompaccomplish, name='apcompacomplish'),
    path('ppm/', views.projectpermonth, name='ppm'),

    path('baplist/', views.bap_list, name="baplist"),
    path('apperbudget/<str:pk>/', views.annual_budget, name="apperbudget"),
    path('create_budgetedap/<str:pk>/', views.createBudgetedAP, name="create_budgetedap"),
    path('create_apsummary/<str:pk>/', views.createAPSummary, name="create_apsummary"),
    
    path('apsummaryrpt', views.apsummaryrpt, name="apsummaryrpt"),    
    
    path('budget_list/', views.budgetList, name="budget_List"),
    path('budgetlistsearch/', views.budgetlsearch, name="budgetlistsearch"),
    
    



    path('road_segments/', views.road_segment_list, name="road_segments"),
    path('road_segment_exts/', views.road_segment_ext, name="road_segment_exts"),
    path('roadsegmentdetail/<str:pk>/', views.road_segment_detail, name="roadsegmentdetail"),
    path('condition_survey_form/<str:pk>/', views.create_condition_survey, name="condition_survey_form"),
    path('road_condition_survey_list/', views.coditionlst, name="road_condition_survey_list"),
    path('roadconditionsummary/', views.condition_summary, name="roadconditionsummary"),
    path('bill_of_qty/<str:pk>/', views.boq, name="bill_of_qty"),
    path('road_condition_detail/<str:pk>/', views.road_condition_detail, name="road_condition_detail"),
    path('roadsegext/', views.roadsegext, name="roadsegext"),


    
    path('roadconditionsurvey/', views.create_conditionsurvey, name="roadconditionsurvey"),

    
]
