<template>
  <footer class="footer">
    <div class="container-fluid">
      <nav>
        <ul class="footer-menu">
          <li>
            <router-link :to="{path:'/home'}">Dashboard</router-link>
          </li>
          <li>
            <a target=_blank href="https://github.com/dprasse/ProtoK">Github</a>
          </li>
        </ul>
      </nav>
      <div class="copyright text-center">
        &copy; 2019 ProtoK | David Prasse, David Vu, Jonathan Nguyen.
      </div>
    </div>
  </footer>
</template>
<script>
export default {};
</script>
<style>

</style>
