# Packet 06 — CI/CD with act / 로컬 CI·CD (Q6)

### 전제
Packet 05 완료 (kind에 앱이 뜸).

### 출처
- homework.md Question 6
- https://nektosact.com/

### 학습 목표
`.github/workflows/ci.yml`: 테스트(+통합, Postgres) → 이미지 빌드 → 통과 시에만 kind 배포. **act**로 로컬 실행. 대시보드 제목을 `Agent Relay v2`로 바꾼 뒤 재실행해 롤아웃 확인.

### 초보자가 할 일
1. 에이전트에게 워크플로 + act 설정을 시킨다 (Docker·kind 접근, 이미지 로드, 고유 태그, 롤아웃 대기).
2. act로 한 번 성공 실행.
3. 대시보드 heading을 `Agent Relay v2`로 변경 후 act 재실행 → 테스트 통과 + 새 제목 확인.
4. Q6 MCQ에 답한다.
5. `AIDT_03_HW.md` 정리 + (선택) Learning in public 초안.

### Coding agent prompt
```text
Create .github/workflows/ci.yml that runs the starter tests and our integration test
against PostgreSQL, builds a Docker image, and deploys to the kind cluster only if tests pass.
Configure running this with act on Windows, including Docker and kind access and loading
the new image into kind. Use a unique image tag per run and wait for rollout.
Then change the dashboard heading to "Agent Relay v2" and help me re-run act to verify.
```

### Q6 선택지
What should happen if a test fails in this workflow?
- Deploy the new version and report the failure.
- Keep the existing version running and stop the deployment.
- Delete the existing deployment.
- Deploy the previous image with the new tag.

### 완료 기준
- [ ] act로 CI 성공
- [ ] v2 heading 롤아웃 확인
- [ ] Q6 + reflection → `AIDT_03_HW.md`

### 하지 말 것
AWS/클라우드 필수화. 숙제는 kind+act까지.
