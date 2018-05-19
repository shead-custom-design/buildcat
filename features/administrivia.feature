Feature: Administrivia

    Scenario:
        Given all sources.
        Then every source must contain a copyright notice.

    Scenario:
        Given all package sources.
        Then every source must contain portability imports.

