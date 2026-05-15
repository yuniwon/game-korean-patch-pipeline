# game-korean-patch-pipeline

AI 에이전트(Claude, Codex)가 게임 한국어 패치를 처음부터 끝까지 진행할 수 있도록 설계된 스킬/파이프라인입니다.

스타샌드 아일랜드, 바하무트 라군 등 실제 프로젝트에서 축적된 노하우를 바탕으로 만들어졌습니다.

## 핵심 원칙

- **발견 → 연구 → 계획 → 번역 → QA → 플레이테스트 → 릴리즈** 순서로 진행
- 사람은 라인별 검토자가 아닌 **테스터** 역할만 담당
- 원본 게임 에셋을 직접 수정하지 않고 **워킹셋** 기반으로 작업
- Steam/Xbox 등 **플랫폼별 분기**를 1등급으로 관리

## 두 가지 모드

- **Bootstrap 모드**: 새 게임 또는 품질이 낮은 기존 번역을 처음부터 시작
- **Maintenance 모드**: 게임 업데이트, 유저 리포트, 플랫폼 분기 이후 기존 패치 유지보수

## 파일 구성

```
SKILL.md                          # 메인 스킬 (Claude / Hermes Agent)
agents/openai.yaml                # Codex 연동 설정
references/
  workflow.md                     # 전체 작업 순서
  research-playbook.md            # 웹 리서치 방법론
  glossary-rules.md               # 용어집 규칙
  category-design.md              # 카테고리 분류 기준
  qa-gates.md                     # QA 체크리스트
  adapter-unity.md                # Unity 엔진 대응
  adapter-unreal.md               # Unreal 엔진 대응
  adapter-table-files.md          # JSON/CSV/TSV 파일 대응
assets/
  glossary_template.tsv           # 용어집 템플릿
  lore_template.md                # 설정집 템플릿
  translation_plan_template.md    # 번역 계획 템플릿
  playtest_report_template.tsv    # 플레이테스트 리포트 템플릿
  release_notice_template_ko.md   # 한국어 배포 공지 템플릿
scripts/
  detect_engine.py                # 엔진 자동 감지
  scan_localization_assets.py     # 로컬라이제이션 에셋 스캔
  build_lore_packet.py            # 설정집 생성
  build_translation_plan.py       # 번역 계획 생성
  build_playtest_report_template.py # 플레이테스트 템플릿 생성
  score_translation_risk.py       # 번역 리스크 점수화
```

## Claude / Hermes Agent에서 사용하기

`SKILL.md`를 스킬로 등록하거나, 대화에서 직접 내용을 참조합니다.

## Codex에서 사용하기

`agents/openai.yaml`을 Codex 에이전트 설정 폴더에 추가합니다.

프로젝트 폴더에 `AGENTS.md`를 만들고 이 레포를 참조하도록 설정하면 Codex가 자동으로 파이프라인을 따릅니다.

## 실제 적용 사례

- [스타샌드 아일랜드 한글패치](https://github.com/yuniwon/starsand-island-korean-patch)
- [Mirage 7 한글패치](https://github.com/yuniwon/mirage7-ko-patch)
- [문스톤 아일랜드 한글패치](https://github.com/yuniwon/moonstone-island-korean-patch)

## 라이선스

MIT
