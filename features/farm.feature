Feature: Farm

    Scenario Outline: No Workers
        Given a buildcat server
        When submitting a "buildcat.worker.info" job
        Then the job count for the "default" queue should be 1

    Scenario: buildcat.worker.info
        Given a buildcat server
        And a buildcat worker
        When submitting a "buildcat.worker.info" job
        Then the job should return worker info
        And the job count for the "default" queue should be 0

