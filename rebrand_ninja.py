#!/usr/bin/env python3

import rebrand_lib as lib

# Three / four letter abbreviation of new block chain. Example: kor, nano, ban
abbreviation = lib.get_env_variable('ABBREVIATION')

domainsvc = lib.get_env_variable('DOMAINSVC')

rep0 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP0')
rep1 = lib.get_env_variable('LIVE_PRE_CONFIGURED_ACCOUNT_REP1')

subdir = "/MyNanoNinja"

ignore_list = [
    "build",
    "git",
    "github",
    "miniupnp",
    "crypto",
    "lmd",
    "gtest",
    "cpptoml",
    "flatbuffers",
    "rocksd",
    "idea",
    "docker",
    "venv",
    "cmake-build-debug",
    "rebrand_nault.py",
    "gitmodules",
    "gitignore",
    "README.md",
    "SECURITY.md",
    "rep_weights_beta",
    "rep_weights_live",
    "clang-format",
    "env_local",
    "env_example",
    "node_modules",
    "nanocurrency-js"
]

sponsorFooter = '''        <li><a href="https://mynano.ninja/account/my-nano-ninja/send">Donate</a></li>
        <li><a href="https://github.com/sponsors/BitDesert">Sponsor</a></li>'''
sponsorFooterReplace = ''
lib.find_and_replace("%s%s/partials/footer.ejs" % (lib.cwd(), subdir),
                 str.encode(sponsorFooter), str.encode(sponsorFooterReplace))


sponsorHeader = '''      <a href="https://github.com/sponsors/BitDesert" class="text-decoration-none" style="color: inherit;">
        <div class="card mb-3">
          <div class="card-body">
            <h5 class="card-title">Sponsor My Nano Ninja!</h5>
            <p class="card-text">
              Donate for the upkeep of the representative and My Nano Ninja page. Thank you for your help!
              <div class="progress" style="height: 2em;">
                <div class="progress-bar progress-bar-smooth" role="progressbar" style="width: 0%" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"><span id="sponsor-progress-text"></span></div>
              </div>
            </p>
          </div>
        </div>
      </a>'''
sponsorHeaderReplace = ''
lib.find_and_replace("%s%s/partials/header.ejs" % (lib.cwd(), subdir),
                 str.encode(sponsorHeader), str.encode(sponsorHeaderReplace))


sponsorNavbar = '''        <li class="nav-item">
          <a class="nav-link" href="https://github.com/sponsors/BitDesert">❤️ Sponsor</a>
        </li>'''
sponsorNavbarReplace = ''
lib.logging.debug(sponsorNavbar)
lib.logging.debug(sponsorNavbarReplace)
lib.find_and_replace("%s%s/partials/navbar.ejs" % (lib.cwd(), subdir),
                 str.encode(sponsorNavbar), str.encode(sponsorNavbarReplace))


updateGoalMain = 'updateGoal();'
updateGoalMainReplace = ''
lib.find_and_replace("%s%s/public/static/js/main.js" % (lib.cwd(), subdir),
                 str.encode(updateGoalMain), str.encode(updateGoalMainReplace))


viewPrincipals = '''  const nf_reps = [
    "nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
    "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
    "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m",
    "nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k",
    "nano_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy",
    "nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
    "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1"
  ];'''
viewPrincipalsReplace = '''  const nf_reps = [
    "{rep0}",
    "{rep1}"
  ];'''.format(rep0=rep0, rep1=rep1)
lib.find_and_replace("%s%s/views/principals.ejs" % (lib.cwd(), subdir),
                 str.encode(viewPrincipals), str.encode(viewPrincipalsReplace))


viewRepresentatives = '''  const nf_reps = [
    "nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4",
    "nano_1stofnrxuz3cai7ze75o174bpm7scwj9jn3nxsn8ntzg784jf1gzn1jjdkou",
    "nano_1q3hqecaw15cjt7thbtxu3pbzr1eihtzzpzxguoc37bj1wc5ffoh7w74gi6p",
    "nano_3dmtrrws3pocycmbqwawk6xs7446qxa36fcncush4s1pejk16ksbmakis78m",
    "nano_3hd4ezdgsp15iemx7h81in7xz5tpxi43b6b41zn3qmwiuypankocw3awes5k",
    "nano_1awsn43we17c1oshdru4azeqjz9wii41dy8npubm4rg11so7dx3jtqgoeahy",
    "nano_1anrzcuwe64rwxzcco8dkhpyxpi8kd7zsjc1oeimpc3ppca4mrjtwnqposrs",
    "nano_1hza3f7wiiqa7ig3jczyxj5yo86yegcmqk3criaz838j91sxcckpfhbhhra1"
  ];'''
viewRepresentativesReplace = '''  const nf_reps = [
    "{rep0}",
    "{rep1}"
  ];'''.format(rep0=rep0, rep1=rep1)
lib.find_and_replace("%s%s/views/statistics/representatives.ejs" % (lib.cwd(), subdir),
                 str.encode(viewRepresentatives), str.encode(viewRepresentativesReplace))

cloudflare = '''    <!-- Cloudflare Web Analytics -->
    <script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "ea11df0588ad483783aef1eccbb1cb9c"}'></script>
    <!-- End Cloudflare Web Analytics -->'''
cloudflareReplace = ''
lib.find_and_replace("%s%s/partials/header.ejs" % (lib.cwd(), subdir),
                 str.encode(cloudflare), str.encode(cloudflareReplace))

googletagmanager = '''    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=UA-115902726-3"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'UA-115902726-3');
    </script>'''
googletagmanagerReplace = ''
lib.find_and_replace("%s%s/partials/header.ejs" % (lib.cwd(), subdir),
                 str.encode(googletagmanager), str.encode(googletagmanagerReplace))

representativeFooter = '<p class="truncate">Representative: <a href="https://mynano.ninja/account/my-nano-ninja">nano_1ninja7rh37ehfp9utkor5ixmxyg8kme8fnzc4zty145ibch8kf5jwpnzr3r</a></p>'
representativeFooterReplace = ''
lib.find_and_replace("%s%s/partials/footer.ejs" % (lib.cwd(), subdir),
                 str.encode(representativeFooter), str.encode(representativeFooterReplace))

words = [
    [b"nano_", b"%s_" % str.encode(abbreviation)],
    [b"|nano", b"|%s" % str.encode(abbreviation)],
    [b"https://mynano.ninja/api/", b"https://%s-ninja.%s/api/" % (str.encode(abbreviation), str.encode(domainsvc))],
    [b"Nano cryptocurrency!", b"%s cryptocurrency!" % str.encode(abbreviation.upper())],
]
lib.replace_all(words, ignore_list, subdir)

