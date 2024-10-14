# config/constants.py
CHROME_BROWSER="chrome"
FIREFOX_BROWSER="firefox"

LENNAR_BASE_URL="https://www.lennar.com"
DRHORTON_BASE_URL="https://www.drhorton.com"

# URLs
LENNAR_SEARCH_URL = "https://www.lennar.com/new-homes/north-carolina/raleigh"

DRHORTON_SEARCH_BOX_ID = "map-search"
DRHORTON_SEARCH_RESULT_TARGET_ID = "ui-id-4"
# HTML Selectors for DR Horton
DRHORTON_COMMUNITY_CARD_CLASS = "CoveoResultLink"
DRHORTON_COMMUNITY_ADDRESS_CLASS = "home-info__address"
DRHORTON_COMMUNITY_PRICE_CLASS = "home-info__from"
DRHORTON_COMMUNITY_TYPE_CLASS = "home-info__stats"
DRHORTON_COMMUNITY_AREA_CLASS = "home-info__square-foot"
DRHORTON_COMMUNITY_AVAILABLE_HOMES_CLASS = "home-info__available-homes"
DRHORTON_COMMUNITY_ABOUT_CLASS = "community-main-details_about"
DRHORTON_COMMUNITY_AMENITIES_CLASS = "amenities"
DRHORTON_COMMUNITY_SCHOOLS_CLASS = "schools"
DRHORTON_COMMUNITY_AREA_INFO_CLASS = "area-info"

DRHORTON_COMMUNITY_FLOORPLANS_ID = "floorplanItems"
DRHORTON_COMMUNITY_AREA_INFO_ID = "areainfo"
DRHORTON_COMMUNITY_AVAILABLE_HOMES_ID = "available-homes"
DRHORTON_COMMUNITY_NEARBY_COMMUNITIES_ID = 'nearbys'
DRHORTON_COMMUNITY_PRIVACY_NOTICE_ID = 'onetrust-banner-sdk'
DRHORTON_COMMUNITY_PAGINATION_BUTTON_CLASS = 'pagination__button'

LENNAR_GRAPHQL_API_URL = "https://www.lennar.com/api/graphql"
LENNAR_SEARCH_BOX_ID = "search-field"
LENNAR_SEARCH_RESULT_TARGET_LINK_SELECTOR = "ul.SearchResultSection_resultList__GwF5_ a"
LENNAR_PRIVACY_NOTICE_MODEL_ID = 'onetrust-consent-sdk'
LENNAR_ADBAR_CONTAINER_CLASS = 'MessageBarV2_backgroundAnimatedContainer__n4Xt4'
LENNAR_MODEL_OVERLAY_CLASS = 'Panel_overlay__M2jRh'
LENNAR_COMMUNITY_BUTTON_CLASS = "SearchResultsTabs_tab__ZjaY_"
LENNAR_LOAD_MORE_COMMUNITY_SELECTOR = ".ListSection_loadMore__e9_jP > .Button_root__8nq_L"

LENNAR_COMMUNITY_CARD_CLASS = "CommunityList_card__eSq0u"
LENNAR_COMMUNITY_CARD_LINK_CLASS = "CommunityCard_link__W1Aem"
LENNAR_COMMUNITY_CARD_TITLE_CLASS = "CommunityCard_title__7RbEn"
LENNAR_COMMUNITY_CARD_BADGE_CLASS = "Badge_root__ZGQeh"
LENNAR_COMMUNITY_CARD_STATUS_CLASS = "CommunityCard_status__X2Moq"
LENNAR_COMMUNITY_CARD_PRICE_ADDRESS_CLASS="MetaDetails_metaItem__cdSlg"
LENNAR_COMMUNITY_CARD_OVERVIEW_CLASS = "CommunityCard_overview__gbUOk"
LENNAR_COMMUNITY_AMENITIES_LINK_CLASS = 'a[href*="amenities"]'
LENNAR_COMMUNITY_NEARBY_PLACES_LINK_CLASS = 'a[href*="nearby-places"]'

LENNAR_HOME_LISTING_CONTAINER_CLASS="HomesitesTableNew_tableDesktop__Wtt_n"
LENNAR_HOME_ITEM_CLASS = "HomesitesTableNew_rowButton__EDamq"
LENNAR_HOMESITE_ID_CLASS = "bodycopySmallNew Typography_bodycopySmallNew__4lltu"
LENNAR_HOME_NEARBY_SCHOOLS_CLASS = "SchoolList_item__jCc_G"
LENNAR_HOME_PRICE_SIDEBAR_ID = "sidebar-price"

LENNAR_AMENITIES_ROOT_DIV_CLASS="AmenitiesModalContent_root__AUXpm"
LENNAR_AMENITIES_CONTAINER_CLASS="AmenitiesModalContent_amenity__GVAhf"
LENNAR_AMENITIES_NAME_LABEL_CLASS="AmenitiesModalContentItem_label__7zcqa"
LENNAR_HOME_SITE_ID="homesite-status"
LENNAR_POIS_CONTAINER_CLASS="PointsOfInterestListItem_listItem__cJ17m"
LENNAR_CONTACT_LINK_SELECTOR="a.CallCta_callButton__L3gzJ.Sidebar_callCta__zUoD8"
LENNAR_LINK_ELEMENT_SELECTOR="div.Links_ctaItems__otJis a.CTAList_ctaBtn__5EewU"
LENNAR_HOME_DETAILS_WRAPPER_CLASS = "HomesiteDetailsInfoV2_supplementalAddressWrapper__k0gEc"

# HTTP headers (for requests)
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
