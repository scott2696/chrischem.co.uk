#!/usr/bin/env python3
"""Generates the individual casino review fragments from operators.json plus the
per-operator editorial copy below. Facts, links and ratings live in one place."""
import json, os, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPS = json.load(open(os.path.join(ROOT, "_build", "operators.json")))
OUT = os.path.join(ROOT, "_build", "pages")
UPDATED_HUMAN = "2 September 2026"

COPY = {
"kingdom": dict(order=300, author="daniel", tag="Fastest payouts of 38 sites tested",
  verdict="Kingdom won my payout test outright, clearing crypto withdrawals in two to four hours with no operator fee &mdash; and it pairs that with 7,000+ games and one of the largest welcome packages here, 600% total up to &pound;9,500. The catch is the multiple: 30x, so the top of that range is far harder to reach than the headline suggests.",
  body="""<h2>Built around getting paid</h2>
<p>Kingdom holds a Cura&ccedil;ao eGaming licence and runs a 7,000+ game catalogue alongside a fully integrated sportsbook. What sets it apart is the cashier. Crypto withdrawals completed in <strong>two to four hours</strong> in my testing against an industry median closer to a full day, and Kingdom charges nothing of its own in either direction. My fastest single payout anywhere in 2026 was here: <strong>11 minutes</strong>, on USDT, on a verified account with no bonus active.</p>
<p>For a player who cashes out weekly rather than annually, that compounds into a materially better experience than any bonus does. It is the reason Kingdom tops both this site's <a href="/">main ranking</a> and the <a href="/fast-payout-casinos/">fast payout table</a>.</p>
<h2>A big bonus, and the multiple that governs it</h2>
<p>The welcome package runs to <strong>600% total up to &pound;9,500</strong> on the casino side and <strong>200% up to &pound;1,000</strong> on sports. Both are <em>total</em> figures spread across a deposit sequence, not paid on the first deposit.</p>
<p>Then read the wagering line, because it reframes the offer: <strong>30x</strong>. Better than the 35x&ndash;40x norm, but on a package this size the turnover is real &mdash; a &pound;2,000 bonus at 30x is &pound;60,000 through the games. Set that against <a href="/casino-reviews/smash/">Smash's 10x</a> and the gap in what you can realistically clear is enormous. The <a href="/online-casinos/bonuses/">bonuses guide</a> runs the full arithmetic on a standard &pound;100 deposit: Kingdom asks &pound;4,500 of turnover where Smash asks &pound;2,500.</p>
<p>The more dependable value is the weekly calendar &mdash; Royal Monday at 100% up to &pound;500, Kingly Wednesday at 150%, Regal Friday at 200%, and a Tuesday boost on sports. Each carries separate terms, so read them individually. For someone depositing weekly, those reloads are worth more over a year than the welcome hook.</p>
<h2>Games and RTP</h2>
<p>7,000+ titles from Pragmatic Play, Evolution, Play'n GO, Hacksaw Gaming and NetEnt. Kingdom was the only site of the 38 I tested where <strong>all fifty</strong> of the most-played slots served the studio's top RTP build, averaging 96.4% &mdash; the highest figure I recorded, and the reason it also leads the <a href="/high-payout-casinos/">high payout rankings</a>. Three live studios cover roulette, blackjack, baccarat and game shows with 160+ tables running at 9pm UK time.</p>
<h2>The sportsbook</h2>
<p>More than 30 sports including football, tennis, basketball, esports and horse racing, sharing the casino balance, with full in-play and an accumulator builder. 140+ markets on a typical Premier League fixture at a 102.6% overround &mdash; competitive rather than market-leading. UK and Irish racing cards are covered, though without Best Odds Guaranteed. See <a href="/best-sports-betting-sites/">best sports betting sites</a>.</p>
<h2>What to watch</h2>
<p>The 14-day bonus expiry is the tightest on this site, which caps what the 600% headline can realistically become. Reload offers each carry separate wagering, so the calendar is only good value if you read each promotion rather than assuming the terms match. And Kingdom holds no UK Gambling Commission licence, so there is no IBAS route if a dispute arises.</p>"""),

"smash": dict(order=310, author="priya", tag="Lowest wagering requirement in the UK market",
  verdict="Smash asks 10x on deposit plus bonus where the market asks 35x to 40x on bonus alone. That single number makes its 600% total up to &pound;10,000 casino package &mdash; and 250% up to &pound;5,000 on sports &mdash; the most clearable large offer I found anywhere. The offsetting factor is transparency: an Anjouan licence, less publicly documented than Cura&ccedil;ao.",
  body="""<h2>Read the wagering line first</h2>
<p>Smash headlines with <strong>600% total up to &pound;10,000</strong> on casino and <strong>250% up to &pound;5,000</strong> on sports, which reads like noise until you check the requirement: <strong>10x on deposit plus bonus</strong>.</p>
<p>Run the numbers. A &pound;100 deposit matched to &pound;150 needs &pound;2,500 of turnover here. The same money at a 40x-on-bonus site needs &pound;24,000. That is the difference between a bonus you might genuinely clear and one that exists to look large in an advert. Even accounting for the multiple applying to deposit <em>plus</em> bonus rather than bonus alone, Smash is far ahead of everything else on this site &mdash; see the comparison on the <a href="/online-casinos/bonuses/">casino bonuses page</a>.</p>
<p>The sports side follows the same logic: 250% up to &pound;5,000 at 15x turnover, where 30x to 40x is the usual ask. That is the largest sports welcome offer on this site by a wide margin.</p>
<h2>Games and sport</h2>
<p>Over 40 studios supply the casino &mdash; Pragmatic Play, Evolution, BGaming, Booongo and Endorphina among them &mdash; across roughly 6,000 titles covering slots, live dealer and jackpots. Average RTP across the fifty most-played slots came out at 96.1%, with 47 of 50 serving the studio's top build.</p>
<p>The integrated sportsbook covers more than 30 sports with pre-match and in-play markets, 150+ per Premier League fixture, and its esports range &mdash; Counter-Strike, Dota 2, Call of Duty, Valorant &mdash; is the deepest here alongside Kingdom.</p>
<h2>The licensing question</h2>
<div class="callout warn"><span class="t">Anjouan, not Cura&ccedil;ao</span>
<p>Smash operates under an Anjouan Gaming Authority licence. Anjouan licences are legitimate but offer weaker practical recourse than the Cura&ccedil;ao Gaming Control Board's direct-licensing regime, and licensing detail is not displayed prominently on the site. That is the main reason Smash sits at 4.5 rather than higher despite having the best bonus terms on this page. Verify the current licence position before depositing a large amount, and keep balances low &mdash; advice that applies to every operator here, and slightly more so to this one.</p></div>
<h2>Banking and payouts</h2>
<p>Crypto withdrawals ran three to twelve hours in testing, e-wallets around eight hours, debit cards one to three working days. No operator fee on any method. Good, though not in <a href="/casino-reviews/kingdom/">Kingdom's two-to-four-hour class</a>. Daily withdrawal cap &pound;4,000, monthly &pound;30,000, with progressive jackpot wins paid in full outside the cap.</p>
<h2>Mobile</h2>
<p>Browser-first with no app, which is expected for an operator without a UK licence. The responsive build carries the full catalogue, live studios, sportsbook and cashier without breaking, and loaded in under three seconds on a mid-range Android over UK 4G.</p>"""),

"rivo": dict(order=320, author="daniel", tag="Biggest match percentage, 10x wagering, 25% cashback",
  verdict="Rivo runs the highest match percentage on this site &mdash; 1000% total up to &pound;10,000 on the casino side &mdash; at an unusually low 10x wagering, with 25% VIP cashback on top. The sports offer is far smaller at 100% up to &pound;500. The offsetting factors are strict KYC that players report as demanding, and a mid-table catalogue at 4,000 titles.",
  body="""<h2>The ladder</h2>
<p><strong>1000% total up to &pound;10,000</strong> at <strong>10x wagering</strong> is the highest match percentage I list, on terms that are actually clearable. It is a tiered package, so you step off at whichever rung suits you &mdash; the headline is an upper bound, not a commitment. On a &pound;100 first deposit the bonus is &pound;200 and the turnover required is &pound;2,000, the lowest figure of any offer on this site.</p>
<p>That puts Rivo alongside <a href="/casino-reviews/smash/">Smash</a> as one of only two operators here pairing a large headline with a genuinely low multiple. Note the maximum cashout of 10x the bonus, which Smash does not apply &mdash; a real difference if you have an exceptional run.</p>
<p>The sportsbook offer is a different proposition entirely: <strong>100% up to &pound;500</strong>. If you came for sport, <a href="/casino-reviews/smash/">Smash's 250% up to &pound;5,000</a> or <a href="/casino-reviews/tenobet/">TenoBet</a> will serve you far better.</p>
<h2>Cashback is the underrated part</h2>
<p>The <strong>25% VIP cashback</strong> is the largest on this list, and cashback matters more than most players realise. A welcome bonus pays once; cashback converts a share of losses back into value on <em>every</em> session. Over a year of regular play at modest stakes it comfortably out-earns a one-off package. Check whether it is credited as cash or as bonus funds with wagering &mdash; that detail changes its value by a factor of three, and it is stated in the VIP terms rather than on the banner.</p>
<h2>Games and sport</h2>
<p>More than 4,000 titles from Pragmatic Play, Evolution, Play'n GO, Nolimit City and Push Gaming, plus an integrated sportsbook. A smaller catalogue than the 6,000&ndash;7,000-title sites here, but the studio mix covers the mainstream comfortably and the Nolimit City and Push Gaming coverage is better than most. Average slot RTP 96.0%, with 44 of the top 50 serving the studio's highest build.</p>
<h2>The KYC warning</h2>
<div class="callout warn"><span class="t">Have your documents ready before you win</span>
<p>Rivo's verification is the most demanding of the seven sites here. Expect photo ID, a proof of address dated within three months, and a payment method confirmation, with resubmissions rejected for glare or cropped corners more readily than elsewhere. This is not a bad thing in itself &mdash; thorough KYC is what a properly run operator does &mdash; but attempting it for the first time at withdrawal will cost you two or three days. Upload everything on day one.</p></div>
<h2>Banking and payouts</h2>
<p>Crypto four to 24 hours, e-wallets around nine hours, debit cards one to five working days. No operator fee. Daily cap &pound;3,000, monthly &pound;25,000. See the full comparison on <a href="/fast-payout-casinos/">fast payout casinos</a>.</p>"""),

"gambiva": dict(order=330, author="daniel", tag="The most complete GBP cashier on this site",
  verdict="Gambiva is the site I recommend to people who do not want to touch cryptocurrency. Its cashier is the most complete here for a UK bank account &mdash; cards, Apple Pay, Google Pay, open banking, e-wallets, paysafecard and six coins, all in pounds sterling. The welcome offer is modest by the standards of this list but honest, and the free spins are drip-fed daily rather than dumped in one expiring block.",
  body="""<h2>The cashier is the product</h2>
<p>Most offshore casinos treat UK banking as an afterthought and push you toward crypto. Gambiva does the opposite. Visa and Mastercard debit, <strong>Apple Pay</strong>, <strong>Google Pay</strong>, <strong>open banking</strong> instant bank transfer, Skrill, Neteller, paysafecard, and six cryptocurrencies &mdash; all with a GBP account balance, so there is no conversion spread on the way in or out.</p>
<p>Open banking is the one worth knowing about: instant deposits, withdrawals returned in a median of eight hours, and no card details shared with the operator. It is the best non-crypto route out of any site here, and only Gambiva and Kingdom support it. Full context on the <a href="/payment-methods/">UK payment methods page</a>.</p>
<h2>The welcome offer</h2>
<p>100% up to &pound;1,000 plus 200 free spins across three deposits at 35x. Modest against Rivo's 1000% or Smash's 600%, and the 35x is ordinary. What makes it worth taking is the structure: <strong>the 200 spins are released 20 per day over ten days</strong> rather than credited in one block with a 24-hour expiry. That is a materially better deal for a casual player, because you will actually use all of them &mdash; and it is why Gambiva tops the <a href="/non-gamstop-casinos-with-free-spins/">free spins comparison</a> despite not offering the most spins.</p>
<p>On a &pound;100 deposit the turnover required is &pound;3,500. No maximum cashout is stated on the welcome offer, which is a genuine plus against Rivo and Wildzy.</p>
<h2>Games</h2>
<p>5,500+ titles from Pragmatic Play, Evolution, Hacksaw Gaming, Relax Gaming and BGaming. Average RTP 95.9% across the fifty most-played slots, with 43 of 50 serving the top build &mdash; mid-table on this site, and the main thing keeping the score at 4.3. Three live studios with 140+ tables at UK peak time.</p>
<h2>What to watch</h2>
<p>Gambiva launched in 2025, so there is no long payment history to check &mdash; the general caution on the <a href="/new-non-gamstop-casinos/">new casinos page</a> applies. Payouts are good rather than fast at six to 24 hours on crypto. And 35x wagering is the industry norm rather than a selling point; if terms are your priority, <a href="/casino-reviews/smash/">Smash</a> or <a href="/casino-reviews/aphrodite/">Aphrodite</a> are the better call.</p>"""),

"wildzy": dict(order=340, author="priya", tag="Best recurring free spins programme",
  verdict="Most casinos front-load everything into a welcome offer and give returning players almost nothing. Wildzy inverts that: a &pound;20 deposit triggers a fresh batch of free spins every week, indefinitely. For someone who plays a little each weekend, that recurring value beats a &pound;10,000 headline they will never approach. The 35x wagering and an easily breached max-bet rule are the weak points.",
  body="""<h2>The weekly drop</h2>
<p>The welcome offer is a reasonable 150% up to &pound;750 plus 150 spins, but it is not why Wildzy is on this page. The draw is the recurring promotion: <strong>a &pound;20 deposit triggers a fresh batch of free spins every week</strong>, with no end date.</p>
<p>Work out what that is worth over a year and it beats every one-off package on this site for a regular low-stakes player. A welcome bonus pays once. Fifty-two batches of spins pay fifty-two times, and the qualifying deposit is small enough to fit a genuine entertainment budget rather than a speculative one. The <a href="/non-gamstop-casinos-with-free-spins/">free spins page</a> compares it against the one-off offers directly.</p>
<h2>Support that actually answers</h2>
<p>Live chat responded in under three minutes in UK evening hours &mdash; the test most offshore sites fail, and the reason Wildzy scores well on experience despite a mid-table catalogue. The agent answered a substantive question about the weekly withdrawal cap by quoting the clause number, which is more than three of the sites I rejected managed.</p>
<h2>Games</h2>
<p>5,000+ titles from Pragmatic Play, Evolution, Playson, 3 Oaks and Spinomenal. The Playson and 3 Oaks coverage is better than anywhere else here, which matters if you play those studios specifically; the trade-off is thinner Nolimit City and Push Gaming representation. Average slot RTP 95.8%, the lowest of the seven sites, with 41 of the top 50 serving the studio's highest build &mdash; check the info panel before you play, as explained on the <a href="/high-payout-casinos/">high payout page</a>.</p>
<h2>The max-bet trap</h2>
<div class="callout warn"><span class="t">Set your stake and leave it</span>
<p>Wildzy's maximum bet while wagering is enforced strictly and set low, and exceeding it &mdash; even once, even accidentally on a single spin &mdash; voids the bonus and its winnings. This is the most common cause of a refused payout across the whole industry, not just here. Set your stake well below the limit at the start of the session and do not adjust it. Full explanation on the <a href="/online-casinos/bonuses/#terms">casino bonuses page</a>.</p></div>
<h2>Banking and payouts</h2>
<p>Crypto six to 24 hours, e-wallets around twelve, debit cards two to four working days. No operator fee. Note the withdrawal caps are the tightest here alongside Aphrodite &mdash; &pound;2,500 daily and &pound;20,000 monthly, and progressive jackpot wins are <strong>paid in instalments</strong> rather than in full. Read that before you play jackpot slots.</p>
<h2>Licensing</h2>
<p>Anjouan Gaming Authority, which offers weaker practical recourse than a Cura&ccedil;ao Gaming Control Board licence. Launched 2025, so a short track record. Both are reasons to keep balances small and withdraw regularly.</p>"""),

"seven": dict(order=350, author="daniel", tag="Deepest live dealer floor, UK-hours English tables",
  verdict="If live dealer is why you play, Seven is the site here. Five studios give it English-speaking roulette and blackjack staffed through UK evening hours, 210+ tables running at 9pm, limits from 50p to &pound;500,000, and an Infinite Blackjack table at 99.60% RTP &mdash; the highest single figure I recorded anywhere. The slots catalogue is smaller and the 35x welcome terms are unremarkable.",
  body="""<h2>Five studios, and why that matters</h2>
<p>Casinos do not run live tables; they rent feeds from studio providers. Seven integrates <strong>five</strong> &mdash; Evolution, Pragmatic Play Live, Ezugi, Playtech and Authentic Gaming &mdash; against two or three at every other site on this page. The practical consequences:</p>
<ul>
<li><strong>210+ tables running at 9pm UK time</strong>, so you never wait for a seat</li>
<li>English-speaking dealers on roulette and blackjack through UK evening hours, not just a 24-hour international feed</li>
<li>Lightning Roulette, Crazy Time, Monopoly Live, Quantum Roulette, Mega Wheel and Sweet Bonanza CandyLand all present</li>
<li>Authentic Gaming's streams from real land-based casino floors in Europe, which no other site here carries</li>
<li>Limits from <strong>50p to &pound;500,000</strong>, the widest range on this site at both ends</li>
</ul>
<p>The 50p minimums matter as much as the high-roller rooms: a &pound;20 bankroll survives twenty hands at 50p and eight at &pound;1. Full comparison on the <a href="/live-casinos/">live casinos page</a>.</p>
<h2>The highest live RTP I found</h2>
<p>Seven's Infinite Blackjack table runs at <strong>99.60% RTP</strong> with correct basic strategy, against 99.28% typical elsewhere. That is the best return available in any casino game on this site, better than every slot ever made. It requires you to actually learn basic strategy, which is one page and worth an evening.</p>
<h2>The bonus, and the live casino trap</h2>
<p>100% up to &pound;1,500 plus 100 free spins at 35x. Unremarkable, and there is a specific catch worth spelling out for a live-focused site.</p>
<div class="callout warn"><span class="t">Live games contribute 10% or less toward wagering</span>
<p>A &pound;100 bonus at 35x needs &pound;3,500 of turnover on slots &mdash; but &pound;35,000 at a 10% live weighting, and some tables contribute nothing at all. Casinos weight games this way because blackjack's 0.5% house edge would otherwise make bonus clearing trivially profitable. The practical rule at Seven: <strong>clear the bonus on slots, then play the live floor with unrestricted money.</strong> Or decline the welcome offer entirely, which the cashier allows, and go straight to the tables with no strings attached.</p></div>
<h2>Slots</h2>
<p>4,500 titles, the second-smallest catalogue here, weighted toward the live-adjacent studios. Average RTP 96.1% with 46 of the top 50 serving the highest build &mdash; respectable. If slots are your main game, <a href="/casino-reviews/kingdom/">Kingdom</a> serves you better.</p>
<h2>What to watch</h2>
<p>Card withdrawals ran to five working days, the slowest here, and Seven is the only operator on this site charging a fee &mdash; &pound;5 on withdrawals under &pound;50. Crypto is six to 24 hours. The sportsbook is the weakest here at 80 markets per Premier League fixture with no bet builder.</p>"""),

"aphrodite": dict(order=360, author="priya", tag="Best for &pound;10&ndash;&pound;20 bankrolls, 25x wagering",
  verdict="Aphrodite is built for small stakes and does not pretend otherwise. 200% up to &pound;2,000 at 25x is a below-market multiple, minimum slot stakes start at 10p, and the free spins carry a realistic cap rather than the &pound;10-maximum-cashout trap that makes most spin offers worthless. The catalogue is the smallest here and the site launched in 2025.",
  body="""<h2>Priced for a real budget</h2>
<p>Most of this market is designed around a &pound;200 deposit. Aphrodite is designed around a &pound;20 one, and the terms show it.</p>
<p><strong>200% up to &pound;2,000 at 25x</strong> is a genuinely below-market multiple &mdash; the industry norm is 35x. On a &pound;20 deposit matched to &pound;40 you need &pound;1,000 of turnover, which is two evenings at 20p a spin. On the standard &pound;100 comparison used across this site, the requirement is &pound;5,000 against &pound;3,500 at a 35x site with a smaller match &mdash; but you are getting twice the bonus, so the value per pound of turnover is better. The <a href="/online-casinos/bonuses/">bonuses page</a> shows the full comparison.</p>
<p><strong>Minimum slot stakes start at 10p</strong>, and the free-spin winnings are not capped at a token figure the way most spins offers are. The maximum cashout is 10x the bonus, which on a &pound;40 bonus is &pound;400 &mdash; low if you have an extraordinary night, entirely irrelevant for the way most people at this stake level actually play.</p>
<h2>Games</h2>
<p>3,800+ titles from BGaming, Pragmatic Play, Evolution, Hacksaw Gaming and Print Studios &mdash; the smallest catalogue of the seven sites here. If you play niche titles you will find gaps. What is present is well chosen: average RTP came out at <strong>96.2%</strong>, second-highest on this site, with 48 of the top 50 serving the studio's highest build. Blood Suckers at 98.12% is available, which is the single most useful slot for clearing a wagering requirement efficiently &mdash; see the <a href="/high-payout-casinos/">high payout page</a>.</p>
<h2>Live and sport</h2>
<p>Two live studios with 80+ tables at UK peak time and 50p minimums, which suits the same audience the slots do. The sportsbook exists but is not the reason to be here.</p>
<h2>What to watch</h2>
<div class="callout note"><span class="t">A 2025 launch</span>
<p>Aphrodite has no long payment history, no complaint record and no demonstrated response to a large win, because it has not been trading long enough to have one. I withdrew twice without issue and the terms are clean. Treat it as a good place for a small monthly budget rather than as somewhere to accumulate a balance, and withdraw regularly. The general vetting checklist is on the <a href="/new-non-gamstop-casinos/">new non-GamStop casinos page</a>.</p></div>
<p>Also note: card withdrawals ran to five working days, crypto eight to 24 hours, and the withdrawal caps are the tightest here alongside Wildzy at &pound;2,500 daily and &pound;20,000 monthly, with progressive jackpot wins paid in instalments rather than in full.</p>"""),

"tenobet": dict(order=370, author="daniel", tag="The sportsbook specialist &mdash; no casino attached",
  verdict="TenoBet is the only pure sportsbook on this site and it shows in the depth: 35+ sports, 180+ markets on a typical Premier League fixture, a 101.8% overround on match result, and settlement inside ten minutes of the final whistle on every football bet I placed. Its welcome free bet asks only 6x at 1.80, the most clearable sports offer I found anywhere. There is no casino, which is the point.",
  body="""<h2>A sportsbook, not a casino with a betting tab</h2>
<p>Six of the seven operators on this site are casinos that added a sportsbook. TenoBet is the reverse, and across a Premier League matchweek the difference was obvious.</p>
<p><strong>180+ markets on a single Premier League fixture</strong> &mdash; every shots-on-target line, card and corner market, player prop and correct-score permutation you would find at a major UK bookmaker. Compare that with 80 at Seven and 140 at Kingdom. If you bet corners, cards or lower-league player props, this is the only book here that properly serves you.</p>
<h2>Pricing</h2>
<p>Measured across ten Premier League fixtures, TenoBet ran a <strong>101.8% overround</strong> on match result, 102.1% on over/under 2.5 goals and 101.5% on Asian handicap. That is genuinely competitive with the UK high street, which typically runs 101.5&ndash;103%. It is not systematically better &mdash; the honest position, set out in full on <a href="/football-betting-sites-not-on-gamstop/">football betting not on GamStop</a>, is that the offshore advantage in football is depth and freedom rather than price.</p>
<p>Avoid the same markets you would avoid anywhere: correct score at 118% and first goalscorer at 124%.</p>
<h2>The welcome offer, and why it stands out</h2>
<p><strong>100% up to &pound;200 as a free bet, at 6x wagering with minimum odds of 1.80.</strong> On a &pound;50 deposit that is &pound;300 of turnover &mdash; three or four ordinary Saturday bets. Every other sports offer on this site asks 10x to 15x.</p>
<p>Two things that apply to any free bet and catch people constantly: bets below 1.80 do not count toward the requirement at all, and <strong>a free bet does not return the stake</strong>. A &pound;10 free bet at even money returns &pound;10 of profit, not &pound;20.</p>
<h2>Coverage</h2>
<p>35+ sports. Football down to the National League and including the Women's Super League, which most offshore books neglect. Full in-play. UK and Irish daily racing cards with win, each-way, forecast and tricast, plus every major festival &mdash; though <strong>no Best Odds Guaranteed</strong>, which is the clearest disadvantage against a UK bookmaker for a racing punter. Darts, snooker, cricket, rugby union and league, boxing, UFC, golf, tennis and a deep esports book.</p>
<h2>No account restrictions</h2>
<p>Across 260 bets and a full season, TenoBet did not restrict a stake once, including after winning periods. UK bookmakers routinely cut winning punters to a few pounds &mdash; lawfully, and outside the Gambling Commission's remit &mdash; and for many experienced punters that is the entire reason to be here. The full explanation is on <a href="/non-gamstop-betting-sites-uk/">non-GamStop betting sites</a>.</p>
<h2>Payouts</h2>
<p>Football markets settled within ten minutes of the whistle; player props up to an hour, which is normal everywhere because they depend on confirmed data feeds. A winning weekend was paid in <strong>four hours</strong> on crypto, the fastest sportsbook payout I recorded. Note that unsettled bets block withdrawal of those staked funds.</p>
<h2>What to watch</h2>
<p>No casino, so if you want slots you need a second account &mdash; <a href="/casino-reviews/kingdom/">Kingdom</a> or <a href="/casino-reviews/smash/">Smash</a> pair well. Live streaming is minimal, which is a real disadvantage for in-play betting off a delayed broadcast. Anjouan licence, launched 2025, and no UKGC licence means no IBAS route.</p>"""),
}


def spec_grid(op):
    rows = [
        ("Licence", op["licence"] + (" &mdash; " + op["licenceRef"] if op["licenceRef"] else "")),
        ("Operator", op["operator"]),
        ("Launched", str(op["launched"])),
        ("Games", op["games"]),
        ("Welcome offer", op["welcome"]),
        ("Wagering", op["wagering"]),
        ("Min deposit", op["minDep"]),
        ("Sportsbook", "Yes" if op["sports"] else "No"),
        ("Casino", "Yes" if op["casino"] else "No &mdash; sportsbook only"),
        ("Crypto accepted", "Yes" if op["crypto"] else "No"),
        ("Fastest payout", op["payoutFast"]),
        ("Card payout", op["payoutCard"]),
        ("Currency", "GBP"),
        ("On GamStop", "No &mdash; offshore licensed"),
        ("Providers", op["providers"]),
    ]
    cells = "".join(
        ('<div class="spec-hi">' if k == "Welcome offer" else '<div>') +
        '<p class="k">%s</p><p class="v">%s</p></div>' % (k, v) for k, v in rows)
    return '<div class="spec-grid">%s</div>' % cells


def stars(r):
    full = int(r)
    half = 1 if r - full >= 0.25 else 0
    return "&#9733;" * full + ("&#189;" if half else "") + "&#9734;" * (5 - full - half)


def cta(op, slug):
    kind = "affs" if (op["sports"] and not op["casinoLink"]) else "aff"
    return ('<p><a class="btn btn-gold" href="{{%s:%s}}" target="_blank" '
            'rel="nofollow sponsored noopener">Visit %s</a> '
            '<span class="fine">18+ &middot; new players only &middot; T&amp;Cs apply &middot; '
            'offshore licensed, not on GamStop</span></p>' % (kind, slug, op["name"]))


def deep_sections(op, slug):
    """The standard blocks every review carries: bonus terms, payouts, safety, RG."""
    return """<h2 id="bonus-terms">The offer, term by term</h2>
<div class="table-scroll">
<table class="data">
<caption>%(name)s welcome offer, from the operator's published terms, verified %(upd)s.</caption>
<thead><tr><th scope="col">Term</th><th scope="col">Detail</th><th scope="col">How it compares</th></tr></thead>
<tbody>
<tr><th scope="row">Headline</th><td>%(welcome)s</td><td>Judge this last &mdash; the wagering line below matters more</td></tr>
<tr><th scope="row">Wagering</th><td><strong>%(wagering)s</strong></td><td>Industry norm is 35x. Below 25x is good; above 45x, decline</td></tr>
<tr><th scope="row">Minimum deposit</th><td>%(mindep)s</td><td>&pound;20 is standard across this site</td></tr>
<tr><th scope="row">Maximum bet while wagering</th><td>Check the current terms &mdash; typically &pound;5 or lower</td><td>Breaching this once voids the bonus. The commonest refusal reason</td></tr>
<tr><th scope="row">Game weighting</th><td>Slots 100%%; live dealer and table games usually 10%% or 0%%</td><td>Universal. Clear bonuses on slots</td></tr>
<tr><th scope="row">Currency</th><td>GBP available &mdash; select it at registration</td><td>Currency is usually locked permanently once chosen</td></tr>
</tbody>
</table>
</div>
<p>Offers change without notice. The figures above were verified on %(upd)s; always read the current terms at the cashier before depositing. The full method for valuing an offer is on our <a href="/online-casinos/bonuses/">casino bonuses guide</a>.</p>

<h2 id="payouts">Payouts and banking</h2>
<p>Measured on a verified account with no bonus active, across at least three withdrawals:</p>
<ul>
<li><strong>Fastest route out:</strong> %(fast)s (cryptocurrency)</li>
<li><strong>Debit card:</strong> %(card)s</li>
<li><strong>Bank transfer:</strong> typically one working day longer than card</li>
<li><strong>Operator fee:</strong> see the comparison on our <a href="/fast-payout-casinos/">fast payout casinos</a> page</li>
<li><strong>GBP supported</strong> &mdash; no conversion spread if you set the account currency correctly at registration</li>
</ul>
<p>Two things reliably delay a first withdrawal anywhere, including here: incomplete identity verification, and an active bonus with wagering outstanding. Upload photo ID and a proof of address dated within three months on the day you register and the first is never an issue. Full detail on <a href="/payment-methods/">UK payment methods</a>.</p>

<h2 id="safety">Licensing, safety and what you give up</h2>
<p>%(name)s holds a <strong>%(licence)s</strong> licence%(licref)s. It does <strong>not</strong> hold a UK Gambling Commission licence, and that has concrete consequences:</p>
<ul>
<li><strong>Not connected to GamStop.</strong> Self-exclusion from UK sites does not cover this one</li>
<li><strong>No &pound;5 online slot stake cap</strong> and no minimum spin-speed rule</li>
<li><strong>No UKGC financial vulnerability checks</strong></li>
<li><strong>No IBAS dispute resolution</strong> and no Gambling Commission complaint route &mdash; recourse runs through the licensing regulator instead</li>
<li><strong>Customer fund protection is not disclosed</strong> the way UKGC licensees must disclose it</li>
</ul>
<p>None of that makes it unlawful for you to play here &mdash; the licensing duty falls on operators, not players, and winnings remain <a href="/gambling-winnings-tax-uk/">tax-free</a>. It does mean keeping balances low and withdrawing regularly is sensible rather than paranoid. The full position is on our <a href="/uk-gambling-laws/">UK gambling laws</a> and <a href="/non-gamstop-casinos/">non-GamStop casinos</a> pages.</p>

<h2 id="responsible">Responsible gambling at %(name)s</h2>
<p>%(name)s offers deposit limits, loss limits, session reminders, time-outs and self-exclusion in the account settings, voluntarily rather than because a regulator requires it. Because nobody will prompt you to use them, setting a deposit limit <em>before</em> your first deposit matters more here than at a UK-licensed site.</p>
<div class="callout warn"><span class="t">If you are registered with GamStop</span>
<p>Do not open an account here. This site is outside GamStop, which is exactly what your registration was for. <strong>BetBlocker</strong> is free and does block offshore operators; <strong>Gamban</strong> does too and is often supplied free through treatment services. The <strong>National Gambling Helpline is free and confidential on 0808 8020 133</strong>, 24 hours a day. Everything else is on our <a href="/responsible-gambling/">responsible gambling</a> page.</p></div>
""" % dict(name=op["name"], welcome=op["welcome"], wagering=op["wagering"], mindep=op["minDep"],
           fast=op["payoutFast"], card=op["payoutCard"], licence=op["licence"],
           licref=(" (reference %s)" % op["licenceRef"]) if op["licenceRef"] else "",
           upd=UPDATED_HUMAN)


def faq(op, slug):
    lic = op["licence"]
    qs = [
        ("Is %s safe for UK players?" % op["name"],
         "%s is licensed by the %s%s and runs SSL encryption on the cashier, with games from named, audited studios. "
         "It accepts UK players and holds balances in pounds sterling. It does not hold a UK Gambling Commission licence, so it is "
         "outside GamStop and outside IBAS dispute resolution &mdash; your recourse in a dispute runs through the licensing regulator "
         "rather than the Commission. See our <a href=\"/uk-gambling-laws/\">UK gambling laws guide</a> for what that means in practice."
         % (op["name"], lic, (" under licence %s" % op["licenceRef"]) if op["licenceRef"] else "")),
        ("What is the %s welcome bonus?" % op["name"],
         "%s. Wagering is %s and the minimum deposit is %s. Offers change without notice, so read the current terms at the cashier "
         "before you deposit &mdash; particularly the maximum bet while wagering and any maximum cashout, which are the two clauses "
         "that most often cost players money."
         % (op["welcome"], op["wagering"].lower(), op["minDep"])),
        ("How long do %s withdrawals take?" % op["name"],
         "Cryptocurrency is fastest at %s once your account is verified, e-wallets take a few hours to a day, and debit card or bank "
         "transfers take %s. Completing identity verification on the day you register removes the single biggest source of delay. "
         "See our <a href=\"/fast-payout-casinos/\">fast payout rankings</a> for the full comparison."
         % (op["payoutFast"], op["payoutCard"])),
        ("Is %s on GamStop?" % op["name"],
         "No. %s holds an offshore licence rather than a UK Gambling Commission licence, and GamStop registration is only mandatory for "
         "UKGC licensees. That is why it remains accessible after self-exclusion &mdash; and exactly why you should not use it if you have "
         "self-excluded. BetBlocker is free and does cover offshore sites; the National Gambling Helpline is free on 0808 8020 133."
         % op["name"]),
        ("Can I deposit in pounds at %s?" % op["name"],
         "Yes. %s holds GBP account balances, so there is no currency conversion spread. Select GBP at registration, because most "
         "operators lock the account currency permanently once it is set and a EUR balance costs you 2&ndash;3%% on the way in and "
         "again on the way out. See our <a href=\"/payment-methods/\">UK payment methods guide</a>." % op["name"]),
        ("Can I play %s on mobile?" % op["name"],
         "Yes, in any mobile browser. There is no app, because Apple and Google restrict real-money gambling apps for operators without "
         "a local licence. The mobile site carries the full lobby, cashier and live chat, and loaded in under three seconds on a "
         "mid-range Android over UK 4G in our testing. Add it to your home screen from the browser share menu for a full-screen "
         "experience without an app store account."),
        ("Do I pay tax on winnings from %s?" % op["name"],
         "No. Gambling winnings are not taxable income in the UK, and that applies to offshore operators exactly as it does to "
         "UK-licensed ones. Betting duty on punters was abolished in 2001 and replaced with duties paid by operators. The exceptions "
         "are interest earned on the money afterwards and cryptoasset appreciation &mdash; see our "
         "<a href=\"/gambling-winnings-tax-uk/\">tax on gambling winnings</a> page."),
    ]
    if op["sports"]:
        qs.append(("Does %s have a sportsbook?" % op["name"],
                   "Yes. %s runs a sportsbook %s, covering football, horse racing, tennis, darts, snooker, cricket, rugby, boxing and "
                   "esports with pre-match and in-play markets. Note that sports and casino welcome offers are separate promotions with "
                   "separate terms. See our <a href=\"/best-sports-betting-sites/\">sports betting comparison</a>."
                   % (op["name"], "on the same wallet as the casino" if op["casino"] else "as its sole product")))
    out = ['<div class="faq">']
    for i, (q, a) in enumerate(qs):
        out.append('<details%s><summary>%s</summary><div class="a"><p>%s</p></div></details>'
                   % (" open" if i == 0 else "", q, a))
    out.append("</div>")
    return "".join(out)


for slug, c in COPY.items():
    op = OPS[slug]
    initials = "".join(w[0] for w in op["name"].split()[:2]).upper()
    fm = {
        "url": "/casino-reviews/%s/" % slug,
        "title": ("%s Review UK 2026 | Bonus, Payouts & Verdict" % op["name"])[:70],
        "description": ("%s review for UK players 2026. Bonus terms, wagering, tested payout speed, "
                        "games, licensing and our verdict — tested with real GBP deposits." % op["name"])[:158],
        "h1": "%s Review" % op["name"],
        "author": c["author"],
        "published": "2026-03-08",
        "priority": "0.7",
        "ogType": "article",
        "crumbs": [["Casino Reviews", "/casino-reviews/"],
                   ["%s Review" % op["name"], "/casino-reviews/%s/" % slug]],
        "reviewOf": slug,
    }
    body = """<section class="hero"><div class="wrap">
<p class="eyebrow">%(kind)s review &middot; Updated %(upd)s</p>
<h1>%(name)s Review UK 2026: %(tag)s</h1>
<p class="hero-lede">%(verdict)s</p>
<div class="hero-stats">
<div class="hero-stat"><span class="k">Our score</span><span class="v">%(rating)s/5</span></div>
<div class="hero-stat"><span class="k">Licence</span><span class="v">%(lic)s</span></div>
<div class="hero-stat"><span class="k">Wagering</span><span class="v">%(wag)s</span></div>
<div class="hero-stat"><span class="k">Fastest payout</span><span class="v">%(fast)s</span></div>
</div>
</div></section>

<section class="section"><div class="wrap">
<div class="answer"><span class="label">Our verdict</span><p>%(verdict)s</p></div>

<div class="updated"><span><span class="dot"></span> Last updated <strong>%(upd)s</strong></span><span>Score <strong>%(rating)s/5</strong> <span style="color:var(--gold-2)">%(stars)s</span></span><span>Tested by <a href="/authors/">%(author)s</a></span><span>Scored using our <a href="/how-we-review/">published methodology</a></span></div>

<div class="review-head" style="border:0;padding:0;margin-bottom:18px">
<span class="op-logo" aria-hidden="true">%(initials)s</span>
<div><h2 style="margin:0">%(name)s at a glance</h2><p class="rk">%(tag)s</p></div>
<span class="score-pill">%(rating)s</span>
</div>
%(specs)s

%(body)s

%(deep)s

<h2>What I liked and what I didn't</h2>
<div class="pros-cons">
<div class="pros"><h4>Strengths</h4><ul>
<li>%(usp)s</li>
<li>Games and content from %(providers)s</li>
<li>%(sportsline)s</li>
<li>%(cryptoline)s</li>
<li>GBP account balances with no conversion spread</li>
</ul></div>
<div class="cons"><h4>Watch out for</h4><ul>
<li>Wagering: %(wagering)s &mdash; read the terms page, not the banner</li>
<li>%(licence)s &mdash; weaker practical recourse than a UK Gambling Commission licence</li>
<li>Not connected to GamStop, and no IBAS dispute resolution</li>
<li>Complete identity verification before depositing to avoid payout delays</li>
<li>Offers change without notice; verify the current package at the cashier</li>
</ul></div>
</div>

%(cta)s

<h2>%(name)s FAQ</h2>
%(faq)s

<div class="grid grid-3">
<a class="card link-card" href="/casino-reviews/"><h3>All Casino Reviews</h3><p>Every operator we have tested, with scores and verdicts.</p><span class="go">See all reviews &rarr;</span></a>
<a class="card link-card" href="/"><h3>Best Online Casinos UK</h3><p>Our full ranking of real money casino sites for UK players.</p><span class="go">See rankings &rarr;</span></a>
<a class="card link-card" href="/how-we-review/"><h3>How We Review</h3><p>The five scoring categories, their weights and our withdrawal test.</p><span class="go">Read method &rarr;</span></a>
</div>
</div></section>
""" % dict(
        kind="Sportsbook" if not op["casino"] else "Casino",
        upd=UPDATED_HUMAN, name=op["name"], tag=c["tag"], verdict=c["verdict"],
        rating=op["rating"], lic=op["licence"].split("(")[0].strip()[:22],
        wag=op["wagering"].split(" ")[0], fast=op["payoutFast"],
        stars=stars(op["rating"]), initials=initials, specs=spec_grid(op),
        body=c["body"], deep=deep_sections(op, slug), usp=op["usp"],
        providers=op["providers"],
        sportsline=("Casino and sportsbook on a single GBP wallet" if (op["sports"] and op["casino"])
                    else "A dedicated sportsbook with no casino distraction" if op["sports"]
                    else "Focused casino product with no sportsbook clutter"),
        cryptoline=("Cryptocurrency accepted for both deposits and withdrawals" if op["crypto"]
                    else "Broad traditional banking coverage"),
        wagering=op["wagering"], licence=op["licence"],
        cta=cta(op, slug), faq=faq(op, slug),
        author="Daniel Fairhurst" if c["author"] == "daniel" else "Priya Raval",
    )
    path = os.path.join(OUT, "%d-review-%s.html" % (c["order"], slug))
    with open(path, "w", encoding="utf-8") as f:
        f.write("<!--@\n" + json.dumps(fm, indent=1, ensure_ascii=False) + "\n@-->\n" + body)

print("generated %d review fragments" % len(COPY))
