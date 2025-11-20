"""
Wordlist builder utilities for generating enriched password dictionaries.
"""
from __future__ import annotations

import itertools
import re
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, Iterator, List, Optional, Sequence, Set, Tuple


@dataclass
class WordlistOptions:
    """Configuration switches for building password candidate streams."""

    use_variations: bool = True
    use_patterns: bool = True
    use_advanced_mangling: bool = False
    use_markov: bool = False
    use_keyboard_walks: bool = False
    max_length: int = 50
    years: Sequence[int] = tuple(range(1990, 2031))
    markov_min_length: int = 4
    markov_max_length: int = 12
    markov_candidate_limit: int = 1000
    markov_branching_factor: int = 5
    keyboard_walk_lengths: Sequence[int] = (3, 4, 5, 6)


class MarkovPasswordGenerator:
    """
    Simple deterministic Markov-chain password generator using bigrams.

    It trains on the base dictionary and then expands the most probable paths
    up to a configurable limit to avoid randomness (useful for reproducibility).
    """

    def __init__(self):
        self._transitions: Dict[str, Counter[str]] = defaultdict(Counter)
        self._start_counts: Counter[str] = Counter()

    def ingest(self, word: str):
        """Update transition counts using the supplied training word."""
        if not word:
            return
        normalized = word.strip()
        if not normalized:
            return
        start_symbol = "^"
        end_symbol = "$"
        prev = start_symbol
        self._start_counts[normalized[0].lower()] += 1
        for ch in normalized.lower():
            self._transitions[prev][ch] += 1
            prev = ch
        self._transitions[prev][end_symbol] += 1

    def generate(
        self,
        *,
        min_length: int,
        max_length: int,
        limit: int,
        branching_factor: int,
    ) -> Iterator[str]:
        """Yield password candidates ranked by Markov likelihood."""
        if not self._transitions:
            return iter(())

        queue: deque[Tuple[str, str]] = deque()
        for start_char, _ in self._start_counts.most_common(branching_factor):
            queue.append(("", start_char))

        yielded = 0
        end_symbol = "$"

        while queue and yielded < limit:
            prefix, prev = queue.popleft()
            if prev == end_symbol:
                continue

            next_chars = self._transitions.get(prev, {})
            if not next_chars:
                continue

            for char, _ in next_chars.most_common(branching_factor):
                if char == end_symbol:
                    if min_length <= len(prefix) <= max_length and yielded < limit:
                        yielded += 1
                        yield prefix
                    continue

                candidate = prefix + char
                if len(candidate) > max_length:
                    continue
                queue.append((candidate, char))


class KeyboardWalkGenerator:
    """Generate keyboard-walk sequences such as qwert, asdfg, qazwsx."""

    ROWS = [
        "1234567890",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
    ]
    DIAGONALS = [
        "1qaz",
        "2wsx",
        "3edc",
        "4rfv",
        "5tgb",
        "6yhn",
        "7ujm",
        "8ik,",
        "9ol.",
        "0p;/",
    ]
    TRAILINGS = ["123", "!", "!@", "!@#", "2024", "2023"]

    @classmethod
    def generate(cls, lengths: Sequence[int]) -> Iterator[str]:
        seen: Set[str] = set()

        def emit(candidate: str):
            lowered = candidate.lower()
            if lowered not in seen:
                seen.add(lowered)
                yield candidate

        for row in cls.ROWS + cls.DIAGONALS:
            row = row.replace(",", "").replace(".", "").replace(";", "").replace("/", "")
            for length in lengths:
                if length > len(row):
                    continue
                for idx in range(len(row) - length + 1):
                    seq = row[idx : idx + length]
                    for variant in (seq, seq[::-1], seq.capitalize(), seq.upper()):
                        yield from emit(variant)
                        for tail in cls.TRAILINGS:
                            yield from emit(variant + tail)


class AdvancedMangling:
    """Additional mangling helpers beyond the basic variation set."""

    DEFAULT_SUBSTITUTIONS = {
        "a": ["4", "@"],
        "e": ["3"],
        "i": ["1", "!"],
        "o": ["0"],
        "s": ["$", "5"],
        "t": ["7"],
    }
    INSERT_SEPARATORS = ("!", ".", "-", "_")

    @classmethod
    def iter_mangles(
        cls,
        base: str,
        *,
        years: Sequence[int],
        substitutions: Optional[Dict[str, List[str]]] = None,
        max_positions: int = 2,
    ) -> Iterator[str]:
        if not base:
            return
        subs = substitutions or cls.DEFAULT_SUBSTITUTIONS
        lowered = base.lower()

        # Multi-position leetspeak substitutions
        indices = [idx for idx, ch in enumerate(lowered) if ch in subs]
        for count in range(1, min(max_positions, len(indices)) + 1):
            for combo in itertools.combinations(indices, count):
                chars = list(lowered)
                for combo_idx in combo:
                    replacements = subs[chars[combo_idx]]
                    for replacement in replacements:
                        chars_copy = chars.copy()
                        chars_copy[combo_idx] = replacement
                        yield "".join(chars_copy)

        mid = len(base) // 2
        for sep in cls.INSERT_SEPARATORS:
            yield base[:mid] + sep + base[mid:]
            if len(base) > 3:
                yield sep.join(re.findall(".{1,2}", base))

        for year in years:
            yield f"{base}{year}"
            yield f"{base}{year}!"
            yield f"{year}{base}"
            yield f"{year}{base}!"


class WordlistBuilder:
    """Build password candidate streams with optional generators."""

    def __init__(self, substitutions: Optional[Dict[str, List[str]]] = None):
        self.substitutions = substitutions or AdvancedMangling.DEFAULT_SUBSTITUTIONS

    def stream_candidates(
        self,
        dictionary_path: str,
        *,
        options: WordlistOptions,
        variation_func: Optional[Callable[[str], Iterable[str]]] = None,
        pattern_func: Optional[Callable[[str], Iterable[str]]] = None,
    ) -> Iterator[str]:
        """
        Yield password candidates from the base dictionary plus optional generators.
        """
        seen: Set[str] = set()
        markov = MarkovPasswordGenerator()

        def add_candidate(candidate: str) -> Optional[str]:
            if not candidate:
                return None
            clean = candidate.strip()
            if not clean:
                return None
            if len(clean) > options.max_length:
                return None
            lowered = clean.lower()
            if lowered in seen:
                return None
            seen.add(lowered)
            return clean

        with open(dictionary_path, "r", encoding="utf-8", errors="ignore") as handle:
            for line in handle:
                base = line.strip()
                if not base:
                    continue
                markov.ingest(base)
                new_candidate = add_candidate(base)
                if new_candidate:
                    yield new_candidate

                if options.use_variations and variation_func:
                    for variation in variation_func(base):
                        normalized = add_candidate(variation)
                        if normalized:
                            yield normalized

                if options.use_patterns and pattern_func:
                    for pattern_pwd in pattern_func(base):
                        normalized = add_candidate(pattern_pwd)
                        if normalized:
                            yield normalized

                if options.use_advanced_mangling:
                    for mangled in AdvancedMangling.iter_mangles(
                        base, years=options.years, substitutions=self.substitutions
                    ):
                        normalized = add_candidate(mangled)
                        if normalized:
                            yield normalized

        if options.use_markov:
            for candidate in markov.generate(
                min_length=options.markov_min_length,
                max_length=options.markov_max_length,
                limit=options.markov_candidate_limit,
                branching_factor=options.markov_branching_factor,
            ):
                normalized = add_candidate(candidate)
                if normalized:
                    yield normalized

        if options.use_keyboard_walks:
            for combo in KeyboardWalkGenerator.generate(options.keyboard_walk_lengths):
                normalized = add_candidate(combo)
                if normalized:
                    yield normalized


