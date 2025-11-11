import { Button, Panel, CellAction, SearchInput } from '@maxhub/max-ui';
import { useState } from 'react';
import './search.css';

const Search = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandedCategory, setExpandedCategory] = useState(null);
  const [showAllRegions, setShowAllRegions] = useState(false);

  const mainPlatforms = [
    {
      id: 1,
      name: 'Федеральный портал проектов НПА (уровень Правительства РФ)',
      url: 'https://regulation.gov.ru/'
    },
    {
      id: 2,
      name: 'Государственная Дума',
      url: 'https://sozd.duma.gov.ru/'
    },
    {
      id: 3,
      name: 'Центральный Банк',
      url: 'https://cbr.ru/project_na/'
    },
    {
      id: 4,
      name: 'Евразийская экономическая комиссия',
      url: 'https://eec.eaeunion.org/'
    }
  ];

  const regions = [
    { name: 'Свердловская область', urls: ['http://regulation.midural.ru/'] },
    { name: 'Республика Адыгея', urls: ['https://regulation.adygeya.ru/'] },
    { name: 'Республика Башкортостан', urls: ['https://regulation.bashkortostan.ru/'] },
    { name: 'Республика Бурятия', urls: ['https://egov-buryatia.ru/minec/activities/zaklyucheniya-ob-otsenke-reguliruyushchego-vozdeystviya-2017.php?clear_cache=Y'] },
    { name: 'Республика Алтай', urls: ['https://orv.mineco04.ru/projects#'] },
    { name: 'Республика Тыва', urls: ['http://mert.tuva.ru'] },
    { name: 'Республика Хакасия', urls: ['https://orv.r-19.ru/rl/'] },
    { name: 'Алтайский край', urls: ['https://altairegion22.ru/gov/pravitelstvo-altayskogo-kraya/administration/stuct/economy/otsenka-reguliruyushchego-vozdeystviya/normativnye-dokumenty-orv/normativnye-dokumenty-altayskogo-kraya/'] },
    { name: 'Республика Дагестан', urls: ['http://dagorv.ru/projects#', 'https://minec.e-dag.ru/activity/7014'] },
    { name: 'Республика Ингушетия', urls: ['https://npa.ingushetia.ru/projects'] },
    { name: 'Кабардино-Балкарская Республика', urls: ['http://regulation.economykbr.ru/projects'] },
    { name: 'Республика Калмыкия', urls: ['https://economy.kalmregion.ru/deyatelnost/orv/'] },
    { name: 'Карачаево-Черкесская Республика', urls: ['https://orv.kchgov.ru/', 'https://economykchr.ru/opot', 'https://economykchr.ru/otsenka-reguliruyushchego-vozdejstviya'] },
    { name: 'Чувашская Республика - Чувашия', urls: ['https://nk.cap.ru/projects'] },
    { name: 'Республика Коми', urls: ['https://econom.rkomi.ru/activity/539/'] },
    { name: 'Республика Карелия', urls: ['https://orv.economy.gov10.ru/'] },
    { name: 'Хабаровский край', urls: ['https://regulation.khv.ru/projects'] },
    { name: 'Чеченская республика', urls: ['https://economy-chr.ru/otsenka-reguliruyushchego-vozdejstviya/zaklyucheniya-ob-orv'] },
    { name: 'Краснодарский край', urls: ['https://regulation.krasnodar.ru', 'https://dirmsp.krasnodar.ru/activity/orv'] },
    { name: 'Республика Татарстан (Татарстан)', urls: ['https://mert.tatarstan.ru/publichnie-konsultatsii.htm'] },
    { name: 'Удмуртская Республика', urls: ['https://regulation.udmr.ru'] },
    { name: 'Красноярский край', urls: ['http://www.krskstate.ru/zakonprojekts/documents?doctype=0&priem_person=0&docs_proc=3&keywords=&searchphrase=exact'] },
    { name: 'Приморский край', urls: ['https://regulation-new.primorsky.ru/'] },
    { name: 'Ставропольский край', urls: ['https://stavinvest.ru/work/evaluation-of-regulatory-impact-in-stavropol-territory/'] },
    { name: 'Амурская область', urls: ['https://or28.amurobl.ru/otsenka-reguliruyushchego-vozdeystviya-or/otsenka-reguliruyushchego-vozdeystviya-proektov-aktov-amurskoy-oblasti/'] },
    { name: 'г. Москва', urls: ['https://www.mos.ru/depr/function/orv-ofv/orv-ofv-rezultaty/rezultaty-v-tekushem-godu/'] },
    { name: 'Астраханская область', urls: ['https://minec.astrobl.ru/directions/ocenka-reguliruyuschego-vozdeystviya-za-2024-god'] },
    { name: 'Белгородская область', urls: ['https://belgorodinvest.com/docs/otsenka-reguliruyushchego-vozdeystviya/'] },
    { name: 'Брянская область', urls: ['https://econom32.ru/activity/ocenka/zakon/'] },
    { name: 'Владимирская область', urls: ['https://regulation.avo.ru/'] },
    { name: 'Волгоградская область', urls: ['https://niktokromenas.volgograd.ru/orv/regional/discussions'] },
    { name: 'Вологодская область', urls: ['http://pravo.gov35.ru/'] },
    { name: 'Воронежская область', urls: ['http://npa.govvrn.ru/'] },
    { name: 'Ивановская область', urls: ['https://derit.ivanovoobl.ru/deyatelnost/otsenka-reguliruyushchego-vozdeystviya/otsenka-reguliruyushchego-vozdeystviya-proektov-npa/proekty-npa/'] },
    { name: 'Иркутская область', urls: ['https://regulation.irkobl.ru', 'https://irkobl.ru/sites/economy/orv/'] },
    { name: 'Калининградская область', urls: ['https://regulation.gov39.ru/'] },
    { name: 'Калужская область', urls: ['https://minek.admoblkaluga.ru/page/orv/', 'http://admoblkaluga.ru/sub/evaluationNPA'] },
    { name: 'Камчатский край', urls: ['https://www.kamgov.ru/minecon/ocenka-reguliruusego-vozdejstvia/publicnye-konsultacii-po-proektam-npa-kamcatskogo-kraa-v-ramkah-ocenki-reguliruusego-vozdejstvia', 'http://regulation.kamgov.ru/'] },
    { name: 'Кемеровская область - Кузбасс', urls: ['https://regulation.kemobl.ru/'] },
    { name: 'Кировская область', urls: ['http://regulation.kirov.ru/'] },
    { name: 'Костромская область', urls: ['https://regulation.kostroma.gov.ru/docs/index.aspx?kind=1'] },
    { name: 'Курганская область', urls: ['https://orv45.ru/'] },
    { name: 'Курская область', urls: ['https://xn--j1aarei.xn--p1ai/region/economy/otsenka-reguliruyushchego-vozdeystviya-i-ekspertiza/'] },
    { name: 'Ленинградская область', urls: ['http://regulation.lenreg.ru/'] },
    { name: 'Липецкая область', urls: ['https://regulation.lipetsk.gov.ru'] },
    { name: 'Магаданская область', urls: ['https://economy.49gov.ru/activities/appraisal/decisions/'] },
    { name: 'Московская область', urls: ['https://regulation.mosreg.ru/projects'] },
    { name: 'Мурманская область', urls: ['https://openregion.gov-murman.ru/acts/'] },
    { name: 'Нижегородская область', urls: ['https://nobl.ru/deyatelnost-pravitelstva/orv/'] },
    { name: 'Новгородская область', urls: ['https://regulation.novreg.ru/projects'] },
    { name: 'Новосибирская область', urls: ['https://dem.nso.ru/npa/bills'] },
    { name: 'Омская область', urls: ['https://regulation.omskportal.ru/Regulation/Materials'] },
    { name: 'Оренбургская область', urls: ['https://regulation.orb.ru/'] },
    { name: 'Орловская область', urls: ['http://regulation.orel-region.ru'] },
    { name: 'Пензенская область', urls: ['https://merp.pnzreg.ru/gosupravlenie/kontrolno-nadzornaya-deyatelnost/orv/zaklyucheniya-ob-orv/'] },
    { name: 'Пермский край', urls: ['https://economy.permkrai.ru/otsenka-reguliruyushchego-vozdeystviya/publichnye-obsuzhdeniya-proektov-npa'] },
    { name: 'Псковская область', urls: ['https://regulation.pskov.ru/projects'] },
    { name: 'Ростовская область', urls: ['https://www.donland.ru/npa-expertise/?filter_disscuss=archive&nav-news=page-1'] },
    { name: 'Рязанская область', urls: ['https://mineconom.ryazan.gov.ru/direction/otsenka_reguliruyushchego_vozdeystviya/zaklyucheniya_i_materialy_ob_otsenke_reguliruyushchego_vozdeystviya/'] },
    { name: 'Самарская область', urls: ['https://regulation.samregion.ru/projects'] },
    { name: 'Саратовская область', urls: ['https://saratov.gov.ru/law/impact/zakl-impact/'] },
    { name: 'Сахалинская область', urls: ['https://orv.sakhalin.gov.ru/projects'] },
    { name: 'Смоленская область', urls: ['https://regulation.admin-smolensk.ru/projects'] },
    { name: 'Тамбовская область', urls: ['https://regulation.tambov.gov.ru/'] },
    { name: 'Тверская область', urls: ['http://orv.tver.ru/'] },
    { name: 'Томская область', urls: ['http://orv-tomsk.ru/publichnye_konsultacii/'] },
    { name: 'Тульская область', urls: ['https://regulation.tularegion.ru/#'] },
    { name: 'г. Санкт-Петербург', urls: ['http://regulation.cipit.gov.spb.ru'] },
    { name: 'Ульяновская область', urls: ['http://73.regportal.pba.su/Regulation/Information/6'] },
    { name: 'Челябинская область', urls: ['https://regulation.ulgov.ru'] },
    { name: 'Забайкальский край', urls: ['https://minek.75.ru/deyatel-nost/ocenka-reguliruyuschego-vozdeystviya/ocenka-proektov/zaklyucheniya-ob-ocenke-reguliruyuschego-vozdeystviya-na-proekty-normativnyh-pravovyh-aktov'] },
    { name: 'Ханты-Мансийский автономный округ - Югра', urls: ['https://depeconom.admhmao.ru/deyatelnost/otsenka-reguliruyushchego-vozdeystviya/'] },
    { name: 'Тюменская область', urls: ['http://regulation.tyumen.gov.ru/regulations/EX/orv.htm'] },
    { name: 'Ямало-Ненецкий автономный округ', urls: ['https://orv.yanao.ru/projects'] },
    { name: 'Еврейская автономная область', urls: ['https://eao.ru/isp-vlast/departament-ekonomiki-pravitelstva-evreyskoy-avtonomnoy-oblasti/otsenka-reguliruyushchego-vozdeystviya/'] },
    { name: 'Архангельская область', urls: ['https://regulation.dvinaland.ru/docs/regulation/'] },
    { name: 'Ненецкий автономный округ', urls: ['https://regulation.adm-nao.ru/'] },
    { name: 'Чукотский автономный округ', urls: ['https://dep.invest-chukotka.ru/orv'] },
    { name: 'Ярославская область', urls: ['https://portal.yarregion.ru/depts-usp/activity/orv/otsenka-reguliruyushchego-vozdeystviya-/'] },
    { name: 'Республика Крым', urls: ['https://minek.rk.gov.ru/structure/4829360c-eb16-4e0e-b884-66647208e947'] },
    { name: 'г. Севастополь', urls: ['https://sev.gov.ru/docs/326/'] },
    { name: 'Республика Саха - Якутия', urls: ['https://xn--14-9kcqjffxnf3b.xn--p1ai/orv/'] },
    { name: 'Республика Марий Эл', urls: ['https://mari-el.gov.ru/ministries/mecon/pages/ozenka-reg-vozdeystvija/#close'] },
    { name: 'Республика Северная Осетия-Алания', urls: ['https://economyrso.ru/publichnye-obsuzhdeniya.html'] },
    { name: 'Республика Мордовия', urls: ['https://mineco.e-mordovia.ru/directions-of-activity/regulatory-impact/opinions-on-ods/index.php'] }
  ];

   const filteredRegions = searchQuery 
    ? regions.filter(region =>
        region.name.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : [];

  const toggleCategory = (categoryId) => {
    setExpandedCategory(expandedCategory === categoryId ? null : categoryId);
  };

  return (
    <div className="search-wrapper">
      <h1>Площадки для публичных консультаций</h1>

      <div className="main-platforms-section">
        <h2>Основные площадки</h2>
        {mainPlatforms.map((platform) => (
          <Panel key={platform.id} mode="secondary" className="platform-panel">
            <div className="platform-content">
              <span className="platform-name">{platform.name}</span>
              <Button
                appearance="themed"
                asChild
                mode="primary"
                size="medium"
              >
                <a
                  href={platform.url}
                  rel="noreferrer"
                  target="_blank"
                >
                  Перейти
                </a>
              </Button>
            </div>
          </Panel>
        ))}
      </div>

      <div className="regions-section">
        <h2>Региональные площадки</h2>
        <div className="search-input-container">
          <SearchInput
            placeholder="Поиск по регионам..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>

        {searchQuery && filteredRegions.length > 0 && (
          <div className="search-results">
            <h3>Результаты поиска:</h3>
            <div className="regions-list">
              {filteredRegions.map((region, index) => (
                <Panel key={index} mode="secondary" className="region-panel">
                  <div className="region-content">
                    <span className="region-name">{region.name}</span>
                    <div className="region-links">
                      {region.urls.map((url, urlIndex) => (
                        <Button
                          key={urlIndex}
                          appearance="themed"
                          asChild
                          mode="primary"
                          size="medium"
                          className="region-link-button"
                        >
                          <a
                            href={url}
                            rel="noreferrer"
                            target="_blank"
                          >
                            {region.urls.length > 1 ? `Ссылка ${urlIndex + 1}` : 'Перейти'}
                          </a>
                        </Button>
                      ))}
                    </div>
                  </div>
                </Panel>
              ))}
            </div>
          </div>
        )}

        {searchQuery && filteredRegions.length === 0 && (
          <Panel mode="secondary" className="no-results-panel">
            <p>Регионы не найдены. Попробуйте изменить запрос.</p>
          </Panel>
        )}

        {!searchQuery && (
          <div className="all-regions-section">
            <Button
              appearance="themed"
              mode="secondary"
              size="large"
              onClick={() => setShowAllRegions(!showAllRegions)}
              className="toggle-regions-button"
            >
              {showAllRegions ? 'Скрыть все регионы' : 'Показать все регионы'}
            </Button>

            {showAllRegions && (
              <div className="regions-list">
                {regions.map((region, index) => (
                  <Panel key={index} mode="secondary" className="region-panel">
                    <div className="region-content">
                      <span className="region-name">{region.name}</span>
                      <div className="region-links">
                        {region.urls.map((url, urlIndex) => (
                          <Button
                            key={urlIndex}
                            appearance="themed"
                            asChild
                            mode="primary"
                            size="medium"
                            className="region-link-button"
                          >
                            <a
                              href={url}
                              rel="noreferrer"
                              target="_blank"
                            >
                              {region.urls.length > 1 ? `Ссылка ${urlIndex + 1}` : 'Перейти'}
                            </a>
                          </Button>
                        ))}
                      </div>
                    </div>
                  </Panel>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;