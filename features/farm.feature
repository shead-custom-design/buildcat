Feature: Farm

    Scenario Outline: Submit jobs programmatically
        Given a running buildcat server
        When submitting a <job> job programmatically
        Then the server should have <count> jobs in the <queue> queue

        Examples:
            | job                       | count     | queue       |
            | "buildcat.worker.info"    | 1         | "default"   |
