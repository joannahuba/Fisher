# **Metodologia**

## **Model symulacyjny**

W pracy zastosowano indywidualno-agentowy model ewolucyjny symulujący dynamikę populacji w zmiennym środowisku. Każdy osobnik reprezentowany jest przez wektor fenotypowy ( p \in \mathbb{R}^n ), a dopasowanie (fitness) zależy od odległości od optymalnego fenotypu środowiska ( \alpha(t) ).

Symulacja przebiega w dyskretnych krokach czasowych (pokoleniach), w których kolejno wykonywane są: mutacja, selekcja, reprodukcja oraz aktualizacja środowiska.

---

## **Fitness i funkcja dopasowania**

Fitness osobnika określany jest za pomocą funkcji Gaussowskiej:

$$
\phi(p, \alpha) = \exp\left(-\frac{|p - \alpha|^2}{2\sigma^2}\right)
$$

gdzie:

* ( p ) — fenotyp osobnika,
* ( \alpha ) — optymalny fenotyp środowiska,
* ( \sigma ) — parametr kontrolujący siłę selekcji.

W przypadku wielu optymalnych fenotypów (np. środowisko wieloszczytowe), fitness definiowany jest jako maksimum:

$$
\phi(p, \alpha_1, \alpha_2, \dots) = \max_i \phi(p, \alpha_i)
$$

---

## **Struktura populacji**

Populacja składa się z ( N ) osobników, z których każdy posiada:

* fenotyp (wektor rzeczywisty),
* możliwość mutacji,
* zdolność do reprodukcji (bezpłciowej lub płciowej).

Populacja jest przechowywana jako zbiór osobników i aktualizowana w każdym pokoleniu poprzez mechanizmy selekcji i reprodukcji.

---

## **Mutacja**

Zastosowano mutację izotropową (isotropic mutation), która działa w dwóch etapach:

1. Z prawdopodobieństwem ( \mu ) osobnik podlega mutacji,
2. Każda cecha fenotypu mutuje niezależnie z prawdopodobieństwem ( \mu_c ),
3. Zmiana wartości cechy dana jest przez:

$$
\Delta p_i \sim \mathcal{N}(0, \xi^2)
$$

Mutacja nie preferuje żadnego kierunku w przestrzeni fenotypów (izotropowość), co odpowiada neutralnemu modelowi zmian genetycznych.

---

## **Selekcja**

Zastosowano dwuetapowy mechanizm selekcji:

### Etap 1: selekcja progowa

Usuwane są osobniki o fitness poniżej ustalonego progu ( \theta ).

### Etap 2: selekcja proporcjonalna

Spośród pozostałych osobników wybierana jest nowa populacja metodą losowania proporcjonalnego do fitness (Wright-Fisher).

Mechanizm ten zapewnia:

* eliminację osobników słabo przystosowanych,
* jednocześnie zachowanie stochastyczności doboru.

---

## **Reprodukcja**

Rozważono dwa typy reprodukcji:

### Reprodukcja bezpłciowa (asexual)

* każdy osobnik reprodukuje się poprzez kopiowanie,
* liczba potomków zależy od losowego wyboru,
* brak rekombinacji genetycznej.

### Reprodukcja płciowa (sexual)

* potomstwo powstaje jako średnia fenotypów dwóch losowo wybranych rodziców,
* następnie dodawana jest mała mutacja gaussowska:
  $$
  p_{child} = \frac{p_1 + p_2}{2} + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma_m^2)
  $$

Reprodukcja wpływa na strukturę populacji i może sprzyjać różnicowaniu fenotypów (potencjalna specjacja).

---

## **Środowisko**

Model środowiska określa dynamikę optymalnego fenotypu ( \alpha(t) ).

### Linear Shift Environment

Optimum zmienia się liniowo w czasie:

$$
\alpha(t) = \alpha(t-1) + c + \eta
$$

gdzie:

* ( c ) — deterministyczny wektor przesunięcia,
* ( \eta \sim \mathcal{N}(0, \delta^2 I) ) — losowe fluktuacje (opcjonalne).

Model ten odpowiada stopniowym zmianom środowiskowym (np. „globalne ocieplenie”).

---

### Alternatywne środowiska

W badaniach mogą być również używane:

* **Shock environment** – okresowe nagłe zmiany optimum,
* **Dual optimum environment** – dwa równoczesne optima, sprzyjające specjacji.

---

## **Kryterium specjacji**

Specjację analizuje się poprzez strukturę przestrzeni fenotypowej populacji.

W szczególności monitorowane są:

* liczba klastrów fenotypów (np. poprzez clustering),
* wariancja fenotypowa,
* rozkład odległości między osobnikami.

Specjacja jest interpretowana jako pojawienie się wyraźnie oddzielonych skupisk fenotypowych w populacji.

---

## **Statystyki symulacji**

W trakcie symulacji zbierane są następujące metryki dla każdego pokolenia:

* średni fitness populacji,
* średni fenotyp,
* wariancja fenotypowa (różnorodność),
* odległość średniego fenotypu od optimum,
* liczba osobników,
* statystyki reprodukcji (liczba rodziców, liczba potomków),
* metryki klasteryzacji (liczba klastrów, silhouette score),
* rozkład fenotypów w czasie.

Dane zapisywane są do plików CSV i wykorzystywane do dalszej analizy statystycznej i wizualizacji.

---

## **Eksperymenty**

Symulacje przeprowadzane są dla różnych konfiguracji parametrów:

* siła mutacji ( \mu, \mu_c, \xi ),
* siła selekcji ( \sigma ),
* typ reprodukcji (aseksualna vs seksualna),
* typ środowiska (linear, shock, dual optimum),
* dynamika środowiska (tempo zmian, fluktuacje).

Każdy eksperyment uruchamiany jest wielokrotnie w celu uwzględnienia losowości procesu ewolucyjnego.

---

## **Analiza danych**

Zebrane dane poddawane są analizie statystycznej obejmującej:

* porównanie średnich metryk między eksperymentami,
* korelacje między różnorodnością a stabilnością populacji,
* analizę zależności między strukturą populacji a specjacją,
* wizualizacje czasowe (trajektorie fenotypów, fitness, clustering).

---

Jeśli chcesz, mogę teraz napisać Ci kolejną sekcję do pracy:

👉 **"Experimental setup + konkretne scenariusze symulacji (baseline, speciation test, shock test itd.)"**
👉 albo **"Results + jak interpretować specjację na wykresach"**
