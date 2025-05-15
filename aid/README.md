# AID

## AID directory structure
- **/datasets**: Has everything for reproducing AID approach. It contains PUTs, program variants, input generators, and reference solutions.
  - **/TrickyBugs**: Data from TrickyBugs dataset.
    - **/p{pid}**: Problem directory.
      - **/variants**: Program variants of PUT.
      - **metainfo.json**: Metadata of the problem. Contains problem URL and its difficulty on AtCoder.
      - **put.py**: PUT(program under test).
      - **ref**: Reference program. Used to obtain ground truth. 
      - **ref.cpp**: Source code of **ref**.
      - **spec.txt**: Specification of the problem.